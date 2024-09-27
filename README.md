# 🚀 Software Development Simulation with AI Agents

Welcome to the **Software Development Simulation** project! This is a fun and interactive way to simulate the process of developing a software project using AI-powered agents. Each agent takes on a specific role within a software development team, such as a **需求分析师** (Requirements Analyst), **系统架构师** (System Architect), **前端开发** (Front-End Developer), **后端开发** (Back-End Developer), **数据库专家** (Database Expert), **测试工程师** (QA Engineer), and **项目经理** (Project Manager).

## 🎉 Introduction

This project is designed to demonstrate how a software development team can collaborate to turn a client's requirements into a fully-fledged software project. The simulation uses OpenAI's API to generate responses based on the role of each agent, ensuring that the output is tailored to the specific responsibilities of each team member.

## 🛠️ How It Works

1. **Input**: You start by providing a detailed software requirement. For example, "开发一个在线书店系统" (Develop an online bookstore system).

2. **Agents**: The system creates a team of agents, each with a specific role. The number of agents can be customized, but it must be at least 2.

3. **Processing**: Each agent processes the requirement in sequence, generating responses that are formatted according to their role. For example, the **需求分析师** will break down the requirements into functional and non-functional components, while the **系统架构师** will design the system architecture.

4. **Final Output**: The **项目经理** (Project Manager) integrates all the suggestions from the team and generates a complete project structure and code.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key (Note: The code currently uses a placeholder `"sk-"` for the API key. You need to replace this with your actual API key.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/software-development-simulation.git
   cd software-development-simulation
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the placeholder API key in the code with your actual OpenAI API key.

### Running the Simulation

1. Run the script:
   ```bash
   python main.py
   ```

2. Follow the on-screen instructions to input the number of agents and the software requirement.

3. Sit back and watch as the AI agents work together to develop your software project!

## 🎨 Customization

- **Agent Roles**: You can customize the roles and their prompts by modifying the `role_prompts` dictionary in the `Agent` class.
- **Colors**: The output is color-coded based on the role of each agent. You can customize these colors by modifying the `role_colors` dictionary.

## 📜 Example Output

Here's a snippet of what the output might look like:

```
--- 开始软件开发流程 ---

[需求分析师的回复]
  1. 功能需求：
    - 用户注册和登录
    - 书籍浏览和搜索
    - 购物车和结账
  2. 非功能需求：
    - 高性能：支持1000并发用户
    - 安全性：数据加密和用户认证
  3. 用户故事：
    - 用户可以注册并登录到系统
    - 用户可以浏览和搜索书籍
    - 用户可以将书籍添加到购物车并结账
  4. 优先级：
    - 用户注册和登录 (高)
    - 书籍浏览和搜索 (高)
    - 购物车和结账 (中)

[系统架构师的回复]
  1. 系统组件：
    - 用户管理模块
    - 书籍管理模块
    - 购物车模块
  2. 技术栈选择：
    - 前端：React
    - 后端：Node.js + Express
    - 数据库：MongoDB
  3. 系统交互图：
    - 用户管理模块与书籍管理模块通过API交互
    - 购物车模块与支付网关通过API交互
  4. 扩展性考虑：
    - 使用微服务架构，便于未来扩展

...

--- 软件开发流程结束 ---

最终项目结构和代码:

1. 项目目录结构：
  - src
    - user
      - User.js
    - book
      - Book.js
    - cart
      - Cart.js
  - public
    - index.html
  - package.json

2. 代码文件：

```文件名: src/user/User.js
// 文件内容
const User = {
  register: function(userData) {
    // 注册逻辑
  },
  login: function(credentials) {
    // 登录逻辑
  }
};

module.exports = User;
```

...
```

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 💬 Contributing

Feel free to fork the project, open a PR, or submit issues and suggestions. Let's make this simulation even more fun and educational!

---

🌟 **Enjoy the simulation and happy coding!** 🌟
