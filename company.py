import asyncio
import os
import signal
import json
import logging
from openai import OpenAI
from termcolor import colored
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print(colored("""
  ______    _     _ _     _      
 |  ____|  | |   | (_)   ( )     
 | |__   __| | __| |_  __|/ ___  
 |  __| / _` |/ _` | |/ __| / __| 
 | |___| (_| | (_| | | (__  \__ \ 
 |______\__,_|\__,_|_|\___| |___/ 
                                                                    
  _____                                    
 / ____|                                   
| |     ___  _ __ ___  _ __   __ _ _ __  _   _ 
| |    / _ \| '_ ` _ \| '_ \ / _` | '_ \| | | |
| |___| (_) | | | | | | |_) | (_| | | | | |_| |
 \_____\___/|_| |_| |_| .__/ \__,_|_| |_|\__, |
                      | |                 __/ |
                      |_|                |___/ 
""", "cyan", attrs=["bold"]))

@dataclass
class AgentConfig:
    name: str
    role: str
    prompt: str
    color: str
    skills: List[str]

class AgentManager:
    def __init__(self):
        self.agents: List[Agent] = []
        self.load_agent_configs()

    def load_agent_configs(self):
        try:
            with open('agent_configs.json', 'r') as f:
                configs = json.load(f)
            for config in configs:
                try:
                    self.agents.append(Agent(**config))
                except Exception as e:
                    logger.error(f"Failed to create agent from config: {config}. Error: {str(e)}")
        except FileNotFoundError:
            logger.error("agent_configs.json file not found. Using default configurations.")
            self._use_default_configs()
        except json.JSONDecodeError:
            logger.error("Invalid JSON in agent_configs.json. Using default configurations.")
            self._use_default_configs()
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading agent configs: {str(e)}")
            self._use_default_configs()

    def _use_default_configs(self):
        default_configs = [
            {"name": "Alice", "role": "需求分析师", "prompt": "分析并明确客户需求", "color": "blue", "skills": ["需求分析", "用户研究"]},
            {"name": "Bob", "role": "系统架构师", "prompt": "设计系统架构", "color": "green", "skills": ["系统设计", "性能优化"]},
            {"name": "Charlie", "role": "前端开发", "prompt": "开发用户界面", "color": "yellow", "skills": ["UI/UX设计", "前端框架"]},
            {"name": "David", "role": "后端开发", "prompt": "实现服务器端逻辑", "color": "magenta", "skills": ["API设计", "数据库优化"]},
            {"name": "Eve", "role": "数据库专家", "prompt": "设计和优化数据库", "color": "cyan", "skills": ["数据建模", "查询优化"]},
            {"name": "Frank", "role": "测试工程师", "prompt": "进行软件测试", "color": "red", "skills": ["自动化测试", "性能测试"]},
            {"name": "Grace", "role": "项目经理", "prompt": "管理项目进度和资源", "color": "white", "skills": ["风险管理", "团队协调"]}
        ]
        for config in default_configs:
            self.agents.append(Agent(**config))

    def get_agent(self, role: str) -> Optional['Agent']:
        return next((agent for agent in self.agents if agent.role == role), None)

    def get_agent_by_skill(self, skill: str) -> Optional['Agent']:
        return next((agent for agent in self.agents if skill in agent.skills), None)

class Agent:
    def __init__(self, name: str, role: str, prompt: str, color: str, skills: List[str]):
        self.name = name
        self.role = role
        self.prompt = prompt
        self.color = color
        self.skills = skills
        self.client = OpenAI(
            api_key="sk-ed6548a7a33541e2b4d0dce50de5f64a",
            base_url="https://api.deepseek.com"
        )
        self.message_history: List[Dict[str, str]] = []
        self.behavior_tree = self._load_behavior_tree()

    def _load_behavior_tree(self):
        try:
            tree_xml = ET.parse(f'{self.role.lower().replace(" ", "_")}_behavior_tree.xml')
            root = tree_xml.getroot()
            return self._xml_to_tree(root)
        except FileNotFoundError:
            logger.warning(f"Behavior tree file for {self.role} not found. Using default behavior.")
            return None

    def _xml_to_tree(self, xml_node):
        # 实现XML到行为树的转换逻辑
        pass

    async def process_message(self, message: str) -> str:
        logger.info(f"{self.name} ({self.role}) 正在处理消息: {message}")
        if self.behavior_tree:
            response = await self._execute_behavior_tree(message)
        else:
            response = await self.get_llm_response(message)
        formatted_response = self.format_response(response)
        self.message_history.append({"role": "user", "content": message})
        self.message_history.append({"role": "assistant", "content": response})
        return formatted_response

    async def _execute_behavior_tree(self, message: str) -> str:
        # 实现行为树执行逻辑
        pass

    async def get_llm_response(self, message: str) -> str:
        try:
            logger.info(f"{self.name} ({self.role}) API调用输入: {message}")
            messages = [
                {"role": "system", "content": f"You are a {self.role} in a software development company with skills in {', '.join(self.skills)}. {self.prompt}"},
                *self.message_history,
                {"role": "user", "content": message}
            ]
            with ThreadPoolExecutor() as executor:
                chat_completion = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: self.client.chat.completions.create(
                        messages=messages,
                        temperature=0.7,
                        model="deepseek-chat",
                        stream=False
                    )
                )
            full_response = chat_completion.choices[0].message.content
            logger.info(f"{self.name} ({self.role}) API调用输出: {full_response.strip()}")
            return full_response.strip()
        except Exception as e:
            logger.error(f"{self.name} ({self.role}) API调用错误: {str(e)}")
            return "抱歉，我现在无法回答这个问题。"

    def format_response(self, response: str) -> str:
        formatted_response = colored(f"[{self.role}的回复]\n", self.color, attrs=["bold"])
        lines = response.split('\n')
        for line in lines:
            formatted_response += colored(f"  {line}\n", self.color)
        return formatted_response.strip()

class SoftwareCompany:
    def __init__(self, n: int):
        self.agent_manager = AgentManager()
        self.agents = self.create_software_company(n)
        self.project_state = {}

    def create_software_company(self, n: int) -> List[Agent]:
        roles = ["需求分析师", "系统架构师", "前端开发", "后端开发", "数据库专家", "测试工程师"]
        agents = [self.agent_manager.get_agent(roles[i % len(roles)]) for i in range(n-1)]
        agents.append(self.agent_manager.get_agent("项目经理"))
        return agents

    async def develop_software(self, client_requirement: str) -> str:
        logger.info(colored("--- 开始软件开发流程 ---", "white", attrs=["bold"]))
        
        self.project_state["requirement"] = client_requirement
        current_message = client_requirement

        for agent in self.agents:
            response = await agent.process_message(current_message)
            print(response)
            self.project_state[agent.role] = response
            current_message += f"\n\n{agent.role}的建议:\n{response}"

        project_manager = self.agents[-1]
        final_request = self.generate_final_request(current_message)
        final_project = await project_manager.get_llm_response(final_request)
        self.project_state["final_project"] = final_project
        logger.info(colored("--- 软件开发流程结束 ---", "white", attrs=["bold"]))
        return final_project

    @staticmethod
    def generate_final_request(current_message: str) -> str:
        return (
            f"根据以下团队成员的建议，生成一个完整的项目结构和代码。请按照以下格式输出：\n"
            "1. 首先列出完整的项目目录结构，每个目录和文件单独一行，使用缩进表示层级关系。\n"
            "2. 然后，对于每个代码文件，使用以下格式：\n\n"
            "```文件名\n"
            "// 文件内容\n"
            "```\n\n"
            "确保每个文件都有清晰的开始和结束标记，并提供完整的代码内容。现在，请根据以下团队成员的建议生成项目：\n"
        ) + current_message

    async def refine_project(self, feedback: str) -> str:
        logger.info(colored("--- 开始项目优化流程 ---", "white", attrs=["bold"]))
        
        current_message = f"项目反馈：{feedback}\n\n当前项目状态：{json.dumps(self.project_state, indent=2)}"
        
        for agent in self.agents:
            response = await agent.process_message(current_message)
            print(response)
            self.project_state[f"{agent.role}_refinement"] = response
            current_message += f"\n\n{agent.role}的优化建议:\n{response}"

        project_manager = self.agents[-1]
        final_request = self.generate_final_request(current_message)
        refined_project = await project_manager.get_llm_response(final_request)
        self.project_state["refined_project"] = refined_project
        logger.info(colored("--- 项目优化流程结束 ---", "white", attrs=["bold"]))
        return refined_project

def signal_handler(signum, frame):
    logger.info("\n程序被强制停止")
    os._exit(0)

async def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            n = int(input("请输入软件公司的员工数量（至少2人，建议3-7人）: "))
            if n < 2:
                logger.warning(colored("员工数量必须至少为2人。请重新输入。", "yellow"))
            elif n > 10:
                logger.warning(colored("员工数量过多可能会影响系统性能。建议不超过10人。是否继续？(y/n)", "yellow"))
                if input().lower() != 'y':
                    continue
            break
        except ValueError:
            logger.error(colored("请输入有效的数字。", "red"))

    company = SoftwareCompany(n)
    
    print(colored("软件需求示例：", "cyan"))
    print("1. 开发一个在线书店系统")
    print("2. 创建一个健康追踪应用")
    print("3. 设计一个智能家居控制平台")
    
    client_requirement = input("请输入您的软件需求（尽量详细描述功能和特点）: ")
    
    result = await company.develop_software(client_requirement)
    print(colored("\n初始项目结构和代码:", "white", attrs=["bold"]))
    print(result)
    
    while True:
        feedback = input("\n请提供项目反馈（或输入'q'退出）: ")
        if feedback.lower() == 'q':
            break
        refined_result = await company.refine_project(feedback)
        print(colored("\n优化后的项目结构和代码:", "white", attrs=["bold"]))
        print(refined_result)
    
    logger.info(colored("程序执行完毕，即将退出。", "cyan"))
    os._exit(0)

if __name__ == "__main__":
    asyncio.run(main())
