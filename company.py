import asyncio
import os
import signal
from openai import OpenAI
from termcolor import colored

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

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.client = OpenAI(
            api_key="sk-",
            base_url="https://api.deepseek.com"
        )
        self.role_prompts = {
            "需求分析师": "作为需求分析师，请分析并细化以下软件需求。输出格式：\n1. 功能需求：[列出主要功能]\n2. 非功能需求：[性能、安全性等]\n3. 用户故事：[描述主要用户场景]\n4. 优先级：[列出功能优先级]",
            "系统架构师": "作为系统架构师，请根据以下需求设计系统架构。输出格式：\n1. 系统组件：[列出主要组件]\n2. 技术栈选择：[前端、后端、数据库等]\n3. 系统交互图：[简要描述组件间交互]\n4. 扩展性考虑：[描述如何支持未来扩展]",
            "前端开发": "作为前端开发工程师，请根据以下需求和架构设计前端代码。输出格式：\n1. 技术栈：[列出使用的前端框架和库]\n2. 组件结构：[描述主要组件及其关系]\n3. 示例代码：[提供关键组件的代码片段]\n4. UI/UX考虑：[描述用户界面和体验设计]",
            "后端开发": "作为后端开发工程师，请根据以下需求和架构设计后端代码。输出格式：\n1. API设计：[列出主要API端点及其功能]\n2. 数据模型：[描述主要数据实体及关系]\n3. 示例代码：[提供关键功能的代码片段]\n4. 性能优化：[描述性能优化策略]",
            "数据库专家": "作为数据库专家，请根据以下需求设计数据库结构。输出格式：\n1. 数据库选择：[推荐的数据库类型及原因]\n2. 表结构设计：[列出主要表及其字段]\n3. 索引策略：[描述主要索引及其用途]\n4. 查询优化：[提供常见查询的优化建议]",
            "测试工程师": "作为测试工程师，请根据以下需求和实现设计测试用例。输出格式：\n1. 功能测试：[列出主要功能的测试用例]\n2. 性能测试：[描述性能测试策略]\n3. 安全测试：[列出安全相关的测试用例]\n4. 自动化测试：[提供自动化测试建议]",
            "项目经理": "作为项目经理，请整合以下团队成员的建议，生成一个完整的项目计划和代码结构。输出格式：\n1. 项目概述：[简要描述项目目标和范围]\n2. 里程碑计划：[列出主要项目里程碑]\n3. 资源分配：[描述团队角色和职责]\n4. 风险管理：[识别潜在风险和缓解策略]\n5. 代码结构：[提供项目的文件夹和文件结构]\n6. 完整代码：[为每个文件提供完整的代码内容]"
        }
        self.role_colors = {
            "需求分析师": "blue",
            "系统架构师": "green",
            "前端开发": "yellow",
            "后端开发": "magenta",
            "数据库专家": "cyan",
            "测试工程师": "red",
            "项目经理": "white"
        }

    async def process_message(self, message):
        print(colored(f"{self.name} ({self.role}) 正在处理消息: {message}", self.role_colors[self.role]))
        response = await self.get_llm_response(message)
        formatted_response = self.format_response(response)
        return formatted_response

    async def get_llm_response(self, message):
        try:
            print(colored(f"{self.name} ({self.role}) API调用输入: {message}", self.role_colors[self.role]))
            role_prompt = self.role_prompts.get(self.role, "")
            chat_completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=[
                    {"role": "system", "content": f"You are a {self.role} in a software development company. {role_prompt}"},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                model="deepseek-chat",
                stream=False
            )
            full_response = chat_completion.choices[0].message.content
            print(colored(f"{self.name} ({self.role}) API调用输出: {full_response.strip()}", self.role_colors[self.role]))
            return full_response.strip()
        except Exception as e:
            print(colored(f"{self.name} ({self.role}) API调用错误: {str(e)}", self.role_colors[self.role]))
            return "抱歉，我现在无法回答这个问题。"

    def format_response(self, response):
        formatted_response = colored(f"[{self.role}的回复]\n", self.role_colors[self.role])
        lines = response.split('\n')
        for line in lines:
            formatted_response += colored(f"  {line}\n", self.role_colors[self.role])
        return formatted_response.strip()

def create_software_company(n):
    roles = ["需求分析师", "系统架构师", "前端开发", "后端开发", "数据库专家", "测试工程师"]
    agents = [Agent(f"Agent{i+1}", roles[i % len(roles)]) for i in range(n-1)]
    agents.append(Agent(f"Agent{n}", "项目经理"))
    return agents

async def develop_software(agents, client_requirement):
    print(colored("--- 开始软件开发流程 ---", "white", attrs=["bold"]))
    
    current_message = client_requirement
    for agent in agents:
        response = await agent.process_message(current_message)
        print(response)
        current_message += f"\n\n{agent.role}的建议:\n{response}"

    project_manager = agents[-1]
    final_request = (
        f"根据以下团队成员的建议，生成一个完整的项目结构和代码。请按照以下格式输出：\n"
        "1. 首先列出完整的项目目录结构，每个目录和文件单独一行，使用缩进表示层级关系。\n"
        "2. 然后，对于每个代码文件，使用以下格式：\n\n"
        "```文件名\n"
        "// 文件内容\n"
        "```\n\n"
        "确保每个文件都有清晰的开始和结束标记，并提供完整的代码内容。现在，请根据以下团队成员的建议生成项目：\n"
    ) + current_message
    final_project = await project_manager.get_llm_response(final_request)
    print(colored("--- 软件开发流程结束 ---", "white", attrs=["bold"]))
    return final_project

def signal_handler(signum, frame):
    print("\n程序被强制停止")
    os._exit(0)

async def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            n = int(input("请输入软件公司的员工数量（至少2人，建议3-7人）: "))
            if n < 2:
                print(colored("员工数量必须至少为2人。请重新输入。", "yellow"))
            elif n > 10:
                print(colored("员工数量过多可能会影响系统性能。建议不超过10人。是否继续？(y/n)", "yellow"))
                if input().lower() != 'y':
                    continue
            break
        except ValueError:
            print(colored("请输入有效的数字。", "red"))

    agents = create_software_company(n)
    
    print(colored("软件需求示例：", "cyan"))
    print("1. 开发一个在线书店系统")
    print("2. 创建一个健康追踪应用")
    print("3. 设计一个智能家居控制平台")
    
    client_requirement = input("请输入您的软件需求（尽量详细描述功能和特点）: ")
    
    result = await develop_software(agents, client_requirement)
    print(colored("\n最终项目结构和代码:", "white", attrs=["bold"]))
    print(result)
    
    print(colored("程序执行完毕，即将退出。", "cyan"))
    os._exit(0)

if __name__ == "__main__":
    asyncio.run(main())
