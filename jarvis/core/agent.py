"""
agent.py - Central Orchestrator Agent for JARVIS
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Callable
from config.settings import settings
from config.constants import PermissionLevel, AIProviderType
from security.credentials import CredentialManager
from core.provider_interface import AIProvider
from core.permissions import PermissionManager
from core.context import SystemContext
from core.memory import ConversationMemory
from core.planner import TaskPlanner, TaskPlan, TaskPlanStep
from tools.registry import tool_registry, ToolResult

class MockAIProvider(AIProvider):
    """Fallback / Offline rule-based AI intent provider for testing or when API key is unconfigured."""

    def generate_response(self, prompt: str, system_prompt: str = "", history: Optional[List[Dict[str, str]]] = None) -> str:
        return "I am JARVIS, your desktop voice assistant. How can I assist you with your computer today?"

    def select_tools(self, user_request: str, available_tools: List[Dict[str, Any]], history: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        req_lower = user_request.lower().strip()

        # Application launch intents
        if req_lower.startswith("open "):
            target = req_lower[5:].strip()
            return [{"name": "open_application", "kwargs": {"app_name": target}}]

        if req_lower.startswith("close "):
            target = req_lower[6:].strip()
            return [{"name": "close_application", "kwargs": {"app_name": target}}]

        if req_lower.startswith("switch to "):
            target = req_lower[10:].strip()
            return [{"name": "open_application", "kwargs": {"app_name": target}}]

        # Browser search / navigation
        if "search brave for" in req_lower:
            query = req_lower.split("search brave for")[-1].strip()
            return [{"name": "open_url", "kwargs": {"url": f"https://www.google.com/search?q={query}"}}]

        if "search youtube for" in req_lower:
            query = req_lower.split("search youtube for")[-1].strip()
            return [{"name": "open_url", "kwargs": {"url": f"https://www.youtube.com/results?search_query={query}"}}]

        if "search the web for" in req_lower or "search web for" in req_lower:
            query = req_lower.replace("search the web for", "").replace("search web for", "").strip()
            return [{"name": "search_web", "kwargs": {"query": query}}]

        # WhatsApp intents
        if "whatsapp" in req_lower or "message" in req_lower:
            if "call" in req_lower:
                parts = req_lower.replace("call", "").replace("on whatsapp", "").replace("whatsapp", "").strip()
                return [{"name": "make_whatsapp_call", "kwargs": {"recipient": parts}}]
            # Parse recipient and message
            # Example: "whatsapp rahul: i will reach at 7" or "send rahul a whatsapp message saying i will reach at 7"
            if ":" in req_lower:
                parts = req_lower.split(":", 1)
                recipient = parts[0].replace("whatsapp", "").replace("send", "").replace("to", "").strip()
                msg = parts[1].strip()
                return [{"name": "send_whatsapp_message", "kwargs": {"recipient": recipient, "message": msg}}]
            if "saying" in req_lower:
                parts = req_lower.split("saying", 1)
                recipient = parts[0].replace("whatsapp", "").replace("send", "").replace("message to", "").replace("a message", "").replace("pe", "").replace("ko", "").strip()
                msg = parts[1].strip()
                return [{"name": "send_whatsapp_message", "kwargs": {"recipient": recipient, "message": msg}}]

        # Gmail intents
        if "check email" in req_lower or "read latest email" in req_lower or "latest email" in req_lower:
            return [{"name": "read_email", "kwargs": {"count": 1}}]

        if "send email to" in req_lower or "email to" in req_lower:
            # Example "send email to Amit"
            target = req_lower.split("to")[-1].strip()
            return [{"name": "send_email", "kwargs": {"recipient": target, "subject": "Update from JARVIS", "body": "Hello, sending update."}}]

        # File management
        if "find pdf" in req_lower or "find my pdf" in req_lower:
            return [{"name": "list_files", "kwargs": {"extension": ".pdf"}}]

        if "downloads folder" in req_lower or "downloads" in req_lower:
            return [{"name": "open_file", "kwargs": {"path": os.path.expanduser("~/Downloads")}}]

        if "create folder" in req_lower:
            folder_name = req_lower.split("folder")[-1].replace("named", "").replace("called", "").strip()
            return [{"name": "create_folder", "kwargs": {"folder_name": folder_name}}]

        # Missed Call & Availability Briefing Intents
        if any(kw in req_lower for kw in ["missed call", "who called", "i'm back", "i am back", "available now", "while i was away"]):
            return [{"name": "check_missed_calls", "kwargs": {}}]

        if req_lower.startswith("record missed call from"):
            parts = req_lower.replace("record missed call from", "").strip()
            caller = parts.split("saying")[0].strip()
            msg = parts.split("saying")[1].strip() if "saying" in parts else ""
            return [{"name": "record_missed_call", "kwargs": {"caller": caller, "message": msg}}]

        # System controls
        if "volume up" in req_lower or "increase volume" in req_lower:
            return [{"name": "control_volume", "kwargs": {"action": "up"}}]
        if "volume down" in req_lower or "turn the volume down" in req_lower or "lower volume" in req_lower:
            return [{"name": "control_volume", "kwargs": {"action": "down"}}]
        if "mute" in req_lower:
            return [{"name": "control_volume", "kwargs": {"action": "mute"}}]
        if "lock my laptop" in req_lower or "lock pc" in req_lower or "lock computer" in req_lower:
            return [{"name": "lock_computer", "kwargs": {}}]
        if "battery" in req_lower or "system info" in req_lower:
            return [{"name": "get_system_info", "kwargs": {}}]

        # Reminders
        if "remind me" in req_lower or "set a reminder" in req_lower:
            return [{"name": "set_reminder", "kwargs": {"text": user_request}}]

        # Default web search for general QA
        return [{"name": "search_web", "kwargs": {"query": user_request}}]

class GeminiAIProvider(AIProvider):
    """Google Gemini AI Provider implementation using google-genai / requests / fallback."""
    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key
        self.model_name = model_name

    def generate_response(self, prompt: str, system_prompt: str = "", history: Optional[List[Dict[str, str]]] = None) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name, system_instruction=system_prompt if system_prompt else None)
            res = model.generate_content(prompt)
            return res.text
        except Exception as e:
            logging.warning(f"[GeminiAIProvider] SDK call failed, using mock provider fallback: {e}")
            return MockAIProvider().generate_response(prompt, system_prompt, history)

    def select_tools(self, user_request: str, available_tools: List[Dict[str, Any]], history: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        # For simplicity and offline reliability, fallback to tool selection logic or structured prompt
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            prompt = f"User Request: '{user_request}'\nAvailable Tools JSON Schemas:\n{json.dumps(available_tools)}\nSelect tool calls. Return valid JSON array of objects with keys 'name' and 'kwargs'."
            model = genai.GenerativeModel("gemini-3.6-flash")
            res = model.generate_content(prompt)
            text = res.text.strip()
            if text.startswith("```json"):
                text = text.split("```json")[1].split("```")[0].strip()
            elif text.startswith("```"):
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
        except Exception as e:
            logging.warning(f"[GeminiAIProvider] Tool selection fallback to mock provider: {e}")
        return MockAIProvider().select_tools(user_request, available_tools, history)

class JARVISAgent:
    """Central orchestrator for input processing, AI intent detection, tool calls, safety checks, and memory."""

    def __init__(self):
        self.memory = ConversationMemory()
        self.ai_provider = self._init_ai_provider()

    def _init_ai_provider(self) -> AIProvider:
        """Initialize selected AI provider."""
        provider_type = settings.ai_provider
        api_key = CredentialManager.get_credential("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") or CredentialManager.get_credential("OPENAI_API_KEY")
        
        if provider_type == AIProviderType.GEMINI.value and api_key:
            logging.info("[JARVISAgent] Initialized Gemini AI Provider.")
            return GeminiAIProvider(api_key=api_key, model_name=settings.ai_model)
        
        logging.info("[JARVISAgent] Using built-in intent engine / Mock AI Provider.")
        return MockAIProvider()

    def process_request(self, user_input: str, confirmation_callback: Optional[Callable[[str, dict, str], bool]] = None) -> Tuple[str, Optional[TaskPlan]]:
        """
        Main pipeline processing user input:
        1. Resolve references ('it', 'first result')
        2. System context gathering
        3. Intent & Tool Selection
        4. Permission Evaluation
        5. Confirmation prompt (if required)
        6. Execution & Verification
        7. Audit Logging & Voice output text creation
        """
        resolved_input = self.memory.resolve_reference(user_input)
        self.memory.add_user_message(resolved_input)

        # Retrieve available tool schemas
        tool_schemas = tool_registry.list_schemas()

        # Select tools to execute
        selected_tool_calls = self.ai_provider.select_tools(resolved_input, tool_schemas, self.memory.get_formatted_history())

        if not selected_tool_calls:
            # General Q&A response
            system_prompt = f"You are JARVIS, an intelligent desktop voice assistant.\n{SystemContext.get_full_context_prompt()}"
            response = self.ai_provider.generate_response(resolved_input, system_prompt, self.memory.get_formatted_history())
            self.memory.add_assistant_message(response)
            return response, None

        # Build Task Plan
        steps = []
        for i, call in enumerate(selected_tool_calls, 1):
            tool_name = call.get("name")
            tool_kwargs = call.get("kwargs", {})
            perm_level, reason = PermissionManager.evaluate(tool_name, tool_kwargs)
            step = TaskPlanStep(
                step_number=i,
                description=f"Execute {tool_name} with {tool_kwargs}",
                tool_name=tool_name,
                tool_params=tool_kwargs,
                permission_level=perm_level.value
            )
            steps.append(step)

        task_plan = TaskPlan(user_command=resolved_input, steps=steps)

        # Execute Plan Steps
        results_summary = []
        for step in task_plan.steps:
            tool_name = step.tool_name
            tool_kwargs = step.tool_params

            # Check if confirmation is required
            if step.permission_level == PermissionLevel.CONFIRM.value:
                confirmed = True
                if confirmation_callback:
                    prompt_msg = f"Before I proceed: Are you sure you want to perform '{tool_name}' with details {tool_kwargs}?"
                    confirmed = confirmation_callback(tool_name, tool_kwargs, prompt_msg)
                
                if not confirmed:
                    step.status = "failed"
                    msg = f"Action '{tool_name}' cancelled by user."
                    self.memory.add_assistant_message(msg)
                    return msg, task_plan

            step.status = "in_progress"
            res: ToolResult = tool_registry.execute_tool(
                name=tool_name,
                user_command=resolved_input,
                mock=settings.mock_mode,
                **tool_kwargs
            )

            if res.success:
                step.status = "completed"
                results_summary.append(res.output)
                self.memory.set_last_tool_output(res.output)
                # Store specific entity memory if present
                if "app_name" in tool_kwargs:
                    self.memory.set_last_app(tool_kwargs["app_name"])
                if "recipient" in tool_kwargs:
                    self.memory.set_last_contact(tool_kwargs["recipient"])
                if "path" in tool_kwargs:
                    self.memory.set_last_file(tool_kwargs["path"])
            else:
                step.status = "failed"
                err_msg = f"Step {step.step_number} ({tool_name}) failed: {res.error}"
                results_summary.append(err_msg)
                break

        final_response = " ".join(results_summary) if results_summary else "Done."
        self.memory.add_assistant_message(final_response)
        return final_response, task_plan
