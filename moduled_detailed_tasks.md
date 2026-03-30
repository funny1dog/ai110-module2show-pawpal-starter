📬 Reminder: Project 2 is due by **Monday, March 30th at 12:59AM MDT**.  
📬 提醒：项目 2 截止日期为 **3 月 30 日星期一凌晨 12：59（山地夏令时** ）。

## Show What You Know: PawPal+  
展示你所知道的：PawPal+

### ℹ️ Project Overview  i️ 项目概述

**⏰ ~4 hours  ⏰ ~4小时**

You've been asked to design PawPal+, a smart pet care management system that helps owners keep their furry friends happy and healthy. The app will track daily routines -- feedings, walks, medications, and appointments -- while using algorithmic logic to organize and prioritize tasks.  
您被要求设计 PawPal+，一套智能宠物护理管理系统，帮助主人保持毛孩子快乐健康。该应用将跟踪日常作息——喂养、散步、用药和预约——同时利用算法逻辑组织和优先排序任务。

Your mission is to move from concept to a working application by designing a modular system architecture using Python’s object-oriented programming (OOP). You will act as the lead architect, using AI to brainstorm your design, scaffold your core logic, and implement sophisticated scheduling algorithms. You will practice a "CLI-first" workflow, ensuring your backend logic in `pawpal_system.py` is robust and verified through a demo script before connecting it to a modern Streamlit UI.  
你的任务是通过使用 Python 的面向对象编程（OOP）设计模块化系统架构，从概念发展到可运行的应用。你将担任首席架构师，利用人工智能头脑风暴设计，构建核心逻辑，并实现复杂的调度算法。你将练习“CLI 优先”的工作流程，确保 `pawpal_system.py` 的后端逻辑稳健且通过演示脚本验证，然后再连接到现代 Streamlit 界面。

#### 🎯 Goals  🎯 目标

By completing this project, you will be able to...  
完成这个项目后，你将能够......

-   Design a modular system using Python classes and visualize relationships with AI-generated Mermaid.js UML diagrams.  
    使用 Python 类设计模块化系统，并通过 AI 生成的 Mermaid.js UML 图示可视化关系。
    
-   Implement OOP principles to represent real-world entities like `Owner`s, `Pet`s, and `Task`s.  
    实现面向对象编程原则，以表示现实世界的实体，如`所有者` 、 `宠物`和`任务` 。
    
-   Develop algorithmic logic for sorting, conflict detection, and recurring task management.  
    开发排序、冲突检测和重复任务管理的算法逻辑。
    
-   Verify system behavior through a CLI demo script and automated `pytest` suites generated with AI assistance.  
    通过 CLI 演示脚本和由 AI 辅助生成的`自动化 pytest` 套件验证系统行为。
    
-   Communicate design intent and reflect on AI-human collaboration tradeoffs in a professional README and consolidated reflection.  
    通过专业的 README 和综合反思，传达设计意图并反思 AI 与人类协作的权衡。
    

***

### ✏️ Project Instructions  ✏️ 项目指示

Phase 1: System Design with UML + AI Support  
第一阶段：支持 UML + AI 的系统设计

**⏰ ~45 mins  ⏰ ~45分钟**

In this phase, you'll design the structure of your PawPal+ app before writing any code. You'll use AI to help brainstorm and visualize the main components (Owner, Pet, Task, Scheduler) and how they connect in a simple UML diagram.  
在这个阶段，你将在编写任何代码之前，先设计 PawPal+ 应用的结构。你将用人工智能帮助头脑风暴和可视化主要组件（主人、宠物、任务、调度器）及其连接方式，绘制一个简单的 UML 图。

**Step 1: Understand the Problem  
第一步：理解问题**

-   Go to the [**PawPal+**](https://github.com/codepath/ai110-module2show-pawpal-starter) repo.  
    去 [**PawPal+**](https://github.com/codepath/ai110-module2show-pawpal-starter) 仓库看看。
    
-   Click **Fork** to create your own copy under your GitHub account, then clone your fork to your computer.  
    点击 **“分支** ”在你的 GitHub 账户下创建自己的副本，然后将你的分支克隆到你的电脑上。
    
-   Clone the fork to your computer, then open the cloned folder in VS Code.  
    把分支克隆到你的电脑上，然后在 VS Code 里打开克隆的文件夹。
    
-   Read the scenario in `README.md` to understand what PawPal+ is intended to do.  
    阅读 `README.md` 中的场景，了解 PawPal+ 的具体目的。
    
-   Identify **three core actions** a user should be able to perform (e.g., add a pet, schedule a walk, see today's tasks).  
    确定用户应能执行**的三个核心动作** （例如，添加宠物，安排散步，查看今天任务）。
    
-   Open `reflection.md` and document these actions in natural language under the **System Design** section.  
    打开 `reflection.md`，并在**系统设计**部分下用自然语言记录这些作。
    

***

**Step 2: List the Building Blocks  
第二步：列出构建模块**

-   Brainstorm the main objects needed for the system. For each object, determine:  
    头脑风暴系统所需的主要物品。对于每个对象，确定：
    
    -   What information it needs to hold (**attributes**)  
        它需要存储哪些信息（ **属性** ）
    -   What actions it can perform (**methods**)  
        它可以执行哪些作（ **方法** ）
    

***

**Step 3: Draft Your UML with AI  
步骤 3：用 AI 起草你的 UML**

-   Open the Copilot Chat in VS Code.  
    在 VS Code 里打开副驾驶聊天。
    
-   Mention you are designing a pet care app with the four classes identified above.  
    提到你正在设计一款包含上述四类宠物护理的应用。
    
-   Ask Copilot to create a Mermaid.js class diagram based on your brainstormed attributes and methods.  
    请 Copilot 根据你头脑风暴的属性和方法绘制一个 Mermaid.js 类图。
    
    Mermaid is a text-based tool that renders diagrams. You can preview Mermaid code in VS Code or paste it into the [**Mermaid Live Editor**](https://mermaid.live/) to see your chart.  
    Mermaid 是一款基于文本的工具，可以渲染图表。你可以在 VS Code 中预览美人鱼代码，或者粘贴到[**美人鱼实时编辑器**](https://mermaid.live/)中查看你的图表。
    
-   Review the diagram. Ensure relationships (like "Owner has Pets") make sense and that you haven't included unnecessary complexity.  
    查看示意图。确保关系（比如“主人有宠物”）合理，且没有加入不必要的复杂内容。
    

***

**Step 4: Translate UML into a Skeleton  
步骤 4：将 UML 转换为骨架**

-   Create a new file named `pawpal_system.py`. This will be your "logic layer" where all your backend classes live.  
    创建一个名为 `pawpal_system.py` 的新文件。这将是你的“逻辑层”，所有后端类都集中在那里。
    
-   Use **Inline Chat** or **Agent mode** to generate the "skeleton" of your classes (the names, attributes, and empty method stubs) based on your UML.  
    使用**内联聊天**或**代理模式** ，根据你的 UML 生成类的“骨架”（名称、属性和空方法存根）。
    
    info Tell Copilot to use **Python Dataclasses** for objects like `Task` and `Pet` to keep your code clean. :::  
    告诉 Copilot 对 `Task` 和 `Pet` 等对象使用 **Python 数据类** ，以保持代码整洁。 :::

-   Commit your draft to GitHub: `git commit -m "chore: add class skeletons from UML"`.  
    请提交您的草稿到 GitHub： `git commit -m "chore: add class skeletons from UML"` 。
    

***

**Step 5: Reflect and Refine  
第五步：反思与精炼**

-   Open `reflection.md`.  
    `reflection.md`。
    
-   Answer section "1a. Initial design" by describing the classes you chose and their responsibilities.  
    回答“1a”部分。通过描述你选择的课程及其职责来描述“初始设计”。
    
-   Ask Copilot to review your skeleton: Use `#file:pawpal_system.py` and ask if it notices any missing relationships or potential logic bottlenecks.  
    让 Copilot 检查你的骨架：使用 `#file:pawpal_system.py`，询问它是否发现任何缺失的关系或潜在的逻辑瓶颈。
    
-   If you make changes based on AI feedback, document what you changed and why in section "1b. Design changes".  
    如果你根据 AI 反馈做出修改，请在“1b.设计变更”部分记录你更改了什么以及原因。
    

📍**Checkpoint**: You've created a clear UML diagram and matching Python class skeletons in `pawpal_system.py`! Your system's blueprint is complete and ready for implementation.  
📍 **检查点** ：你已经创建了一个清晰的 UML 图和匹配的 Python 类骨架，在 `pawpal_system.py` 中！您的系统的蓝图已完成，准备实施。

Phase 2: Core Implementation  
第二阶段：核心实施

**⏰ ~90 mins  ⏰ ~90分钟**

In this phase, you'll translate your UML design into working Python code. You'll follow a "CLI-first" workflow, meaning you'll build and verify your backend logic in a standalone script before touching the Streamlit UI. This ensures your system's "brain" is solid.  
在这个阶段，你将把 UML 设计转化为可运行的 Python 代码。你将遵循“CLI 优先”的工作流程，也就是说，在使用 Streamlit 界面之前，你会在独立脚本中构建并验证后端逻辑。这确保了你系统的“大脑”是稳固的。

**Step 1: Scaffold the Logic Layer  
步骤1：构建逻辑层支架**

Now you'll write the full code for all your main classes.  
现在你要为所有主类写完整代码。

-   Use **Agent Mode** or **Edit Mode** to flesh out the core implementation of your four classes in `pawpal_system.py`  
    使用**代理模式**或**编辑模式**来完善你四个职业的核心实现 `pawpal_system.py`
    
    -   `Task`: Represents a single activity (description, time, frequency, completion status).  
        `任务` ：表示单一活动（描述、时间、频率、完成状态）。
        
    -   `Pet`: Stores pet details and a list of tasks.  
        `宠物` ：存储宠物信息和任务清单。
        
    -   `Owner`: Manages multiple pets and provides access to all their tasks.  
        `主人` ：管理多只宠物，并提供参与它们所有任务的权限。
        
    -   `Scheduler`: The "Brain" that retrieves, organizes, and manages tasks across pets.  
        `调度器` ：“大脑”，负责检索、组织和管理宠物间的任务。
        
        If you aren't sure how a `Scheduler` should "talk" to an `Owner` to get pet data, ask Copilot: "Based on my skeletons in `#file:pawpal_system.py`, how should the `Scheduler` retrieve all tasks from the `Owner`'s pets?"  
        如果你不确定调`度员`应该如何“与`主人`对话”获取宠物数据，可以问 Copilot：“根据我在 `#file:pawpal_system.py` 的骨骼数据， `调度员`应该如何从`主人`的宠物那里获取所有任务？”
        
    

***

**Step 3: Create and Run a Demo Script  
步骤3：创建并运行演示脚本**

-   Create a new file named `main.py`. This is your temporary "testing ground" to verify your logic works in the terminal.  
    创建一个名为 `main.py` 的新文件。这是你临时的“测试地”，用来验证你的逻辑在终端里是否正常。
    
-   Write a script in `main.py` that performs the following:  
    用 `main.py` 写一个脚本，实现以下功能：
    
    -   Imports your classes from `pawpal_system.py`.  
        它会从 `pawpal_system.py` 导入你的职业。
        
    -   Creates an `Owner` and at least two `Pet`s .  
        创建一个`主人`和至少两个`宠物` 。
        
    -   Adds at least three `Task`s with different times to those pets.  
        给这些宠物添加至少三个不同时间的`任务` 。
        
    -   Prints a "Today's Schedule" to the terminal.  
        向终端打印“今日日程表”。
        
    
-   Run your script: `python main.py`.  
    运行你的脚本：`python main.py`。
    
    If your schedule prints out as a messy list of objects, use **Inline Chat** on your print statement and ask: "Suggest a clearer, more readable way to format this schedule output for the terminal".  
    如果你的日程表打印出来时是一堆杂乱的物品，可以用**内联聊天**在打印语句中请求：“建议一个更清晰、更易读的终端排程输出格式化”。
    

***

**Step 4: Add Quick Tests  
步骤4：添加快速测试**

-   Open the terminal and ensure you have `pytest` installed (`pip install pytest`).  
    打开终端，确认你已经安装了 `pytest`（`pip install pytest`）。
    
-   Create a file named `tests/test_pawpal.py`.  
    创建一个名为 `tests/test_pawpal.py` 的文件。
    
-   Use the **Generate tests** smart action or Copilot Chat to draft two simple tests:  
    使用 **“生成测试**智能动作”或 Copilot Chat 来起草两个简单的测试：
    
    -   **Task Completion:** Verify that calling `mark_complete()` actually changes the task's status.  
        **任务完成：** 确认调用 `mark_complete（）` 是否真的改变了任务状态。
        
    -   **Task Addition:** Verify that adding a task to a `Pet` increases that pet's task count.  
        **任务补充：** 确认给`宠物`添加任务是否会增加该宠物的任务数量。
        
    
-   Run your tests by typing `python -m pytest` in the terminal.  
    在终端里输入 `python -m pytest` 来运行测试。
    

***

**Step 5: Document, Reflect, and Merge  
步骤5：记录、反思与合并**

-   Use the **Generate documentation** smart action to add 1-line docstrings to your methods in `pawpal_system.py`  
    使用 **“生成文档**智能作”，在 `pawpal_system.py` 中为你的方法添加一行文档字符串
    
-   Use Copilot's **Generate Commit Message** feature in the Source Control tab to summarize your implementation.  
    在源控制标签页中使用 Copilot 的 **“生成提交消息** ”功能来总结你的实现。
    
-   Push your work: `git push origin main`.  
    推送你的作品：`git 推送 origin main`。
    

📍**Checkpoint**: You've transformed your UML design into a functioning system! Your classes now work together to manage pets, tasks, and schedules, and you've verified them using a CLI demo script and initial automated tests.  
📍 **检查点** ：你已经把你的 UML 设计转化为一个可运行的系统！你的班级现在协同工作，管理宠物、任务和日程，你已经用 CLI 演示脚本和初始自动化测试验证了它们。

Phase 3: UI and Backend Integration  
第三阶段：用户界面与后端集成

**⏰ ~20 mins  ⏰ ~20分钟**

Currently, your logic (`pawpal_system.py`) and your user interface (`app.py`) live in separate worlds. In this phase, you will act as the "bridge" to ensure that when a user clicks a button in the app, your Python classes actually respond.  
目前，你的逻辑（`pawpal_system.py`）和用户界面（`app.py`）存在于不同的世界。在这个阶段，你将充当“桥梁”，确保当用户点击应用中的按钮时，你的 Python 类会真正响应。

**Step 1: Establish the Connection  
第一步：建立联系**

To use the `Owner`, `Pet`, and `Task` classes inside your Streamlit script, you must first make them accessible.  
要在 Streamlit 脚本中使用 `Owner`、`Pet` 和 `Task` 类，首先必须让它们可访问。

-   Use a Python `import` statement to bring specific classes from `pawpal_system.py` into `app.py`.  
    用 Python `导入`语句把 `pawpal_system.py` 里的特定类导入到 `app.py`。
    

***

**Step 2: Manage the Application "Memory"  
步骤2：管理应用程序“内存”**

Streamlit is stateless, meaning it runs your code from top to bottom every time you click a button. If you simply create an `Owner` at the top of the script, it will be "reborn" (and empty) every time the page refreshes.  
Streamlit 是无状态的，意味着每次点击按钮时，它都会从上到下运行你的代码。如果你只是在脚本顶部创建一个`所有者` ，每次页面刷新时它都会“重生”（并且是空的）。

-   Use AI to investigate `st.session_state`. Find out how to check if an object (like your `Owner` instance) already exists in the "vault" of the session before creating a new one.  
    利用人工智能调查 `st.session_state`。在创建新项目之前，先查查某个对象（比如你的 `Owner` 实例）是否已经存在于会话的“vault”里。
    
    Think of `st.session_state` as a dictionary. You want to store your `Owner` object there so your data persists while you navigate the app.  
    把 `st.session_state` 想象成一本词典。你要把`你的所有者`对象存在那里，这样在你浏览应用时数据就能保持。
    

***

**Step 3: Wiring UI Actions to Logic  
步骤 3：将 UI 作接入逻辑**

-   Locate the UI components for "Adding a Pet" or "Scheduling a Task" in `app.py`. Replace those placeholders with calls to the methods you wrote in Phase 2.  
    在 `app.py` 中找到“添加宠物”或“安排任务”的 UI 组件。用你在第二阶段写的方法调用替换那些占位符。
    
    If a user submits a form to add a new pet, which class method should handle that data, and how does the UI get updated to show the change?  
    如果用户提交表单添加新宠物，哪个类方法应该处理这些数据？界面如何更新以显示变更？
    

📍**Checkpoint**: Your `app.py` successfully imports your logic layer! Adding a pet in the browser actually creates a `Pet` object that stays in memory.  
📍 **检查点** ：你的 `app.py` 成功导入了你的逻辑层！在浏览器中添加宠物实际上会创建一个`宠物对象，` 并且会保留在内存中。

Phase 4: Algorithmic Layer  
第四阶段：算法层

**⏰ ~45 mins  ⏰ ~45分钟**

Make your PawPal+ system _smart_! In this phase, you'll add simple algorithms that make your app more functional and intelligent -- sorting, filtering, recurring tasks, and basic conflict detection. You'll ask AI to brainstorm, write, and compare solutions, learning how to evaluate algorithmic choices for clarity and efficiency.  
让你的 PawPal+系统_智能_化！在这个阶段，你将添加简单的算法，使应用更实用和智能——排序、过滤、重复任务以及基础冲突检测。你会让 AI 头脑风暴、编写并比较解决方案，学习如何评估算法选择以提升清晰度和效率。

**Step 1: Review and Plan  
第一步：复习与规划**

-   Review your `main.py` demo from Phase 2. Identify where the current logic feels manual or overly simple.  
    回顾你第二阶段的 `main.py` 演示。找出当前逻辑感觉手动或过于简单的地方。
    
-   Open a **New Chat Session** to keep your algorithmic planning separate from your core implementation.  
    开**启一个新聊天会话** ，将你的算法规划与核心实现分开。
    
-   Use `#codebase` to ask Copilot to suggest a list of small algorithms or logic improvements that could make your scheduling app more efficient for a pet owner.  
    利用 `#codebase` 请求 Copilot 建议一些小型算法或逻辑改进，以提升宠物主人的排班应用效率。
    
-   **Target Features:** You will implement logic for sorting tasks by time, filtering by pet/status, handling recurring tasks, and basic conflict detection .  
    **目标特征：** 你将实现按时间排序任务、按宠物/状态过滤、处理重复任务以及基础冲突检测的逻辑。
    

***

**Step 2: Implement Sorting and Filtering  
步骤2：实现排序和筛选**

-   Open `pawpal_system.py`.  
    `pawpal_system.py`。
    
-   **Sorting Logic:** Use **Inline Chat** on your `Scheduler.sort_by_time()` method to ask for a way to sort your `Task` objects by their time attribute.  
    **排序逻辑：** 在`你的 Scheduler.sort_by_time（）` 方法中使用**内联聊天** ，请求按时间属性`排序任务对象`的方法。
    
    Python's `sorted()` function is powerful. Ask Copilot how to use a `lambda` function as a "key" to sort strings in "HH:MM" format.  
    Python 的 `sorted（）` 函数非常强大。问问 Copilot 如何用 `lambda` 函数作为“键”来排序字符串，格式为“HH：MM”格式。
    
-   **Filtering Logic:** Use **Edit Mode** to implement a method that filters tasks by completion status or pet name.  
    **过滤逻辑：** 使用**编辑模式**实现一种按完成状态或昵称过滤任务的方法。
    
-   Update your `main.py` to add tasks out of order, then print the results using your new sorting and filtering methods to ensure they work in the terminal.  
    更新你的 `main.py`，把任务顺序打乱，然后用新的排序和筛选方法打印结果，确保它们在终端中正常工作。
    

***

**Step 3: Automate Recurring Tasks  
步骤3：自动化重复性任务**

-   Add logic to your `Task` or `Scheduler` class so that when a "daily" or "weekly" task is marked complete, a new instance is automatically created for the next occurrence.  
    为你的`任务`或`调度`类添加逻辑，这样当一个“每日”或“每周”任务被标记为完成时，会自动创建一个新的实例以应对下一次任务。
    
-   Use **Agent Mode** to handle this change, as it may require edits to how `mark_task_complete` interact with the `Task` frequency.  
    使用**代理模式**来处理此变更，因为可能需要修改 `mark_task_complete` 与`任务`频率的交互方式。
    
    If a task happens "Daily," its new due date should be `today + 1 day`. Ask Copilot how to use Python's `timedelta` to calculate this accurately.  
    如果任务是“每日”完成，新的截止日期应为`今天+1 天` 。问问 Copilot 如何用 Python 的时间`差`准确计算。
    

***

**Step 4: Detect Task Conflicts  
步骤4：检测任务冲突**

-   Extend your `Scheduler` to detect if two tasks for the same pet (or different pets) are scheduled at the same time.  
    扩展你的`调度器` ，检测是否同时安排了同一款宠物（或不同宠物）的两个任务。
    
-   Ask Copilot for a "lightweight" conflict detection strategy that returns a warning message rather than crashing the program.  
    向 Copilot 请求一个“轻量级”冲突检测策略，能返回警告信息，而不是让程序崩溃。
    
-   Update `main.py` with two tasks at the same time and verify that your `Scheduler` correctly identifies and prints a warning.  
    同时更新 `main.py` 两个任务，并确认你的`调度器`正确识别并打印警告。
    

***

**Step 5: Evaluate and Refine  
第五步：评估与完善**

-   Share one of your completed algorithmic methods with Copilot and ask: "How could this algorithm be simplified for better readability or performance?".  
    把你完成的算法方法分享给 Copilot，并问：“如何简化这个算法以提升可读性和性能？”
    
-   Review the AI's suggestion. If its version is more "Pythonic" but harder for a human to read, decide which version to keep.  
    请参考 AI 的建议。如果版本更“派森式”但人类难以阅读，就决定保留哪个版本。
    
-   Open `reflection.md` and document one tradeoff your scheduler makes (e.g., only checking for exact time matches instead of overlapping durations) in section "2b. Tradeoffs".  
    打开 `reflection.md`，记录调度员做出的一个权衡（例如，只检查精确时间匹配而非重叠时长），在“2b. 权衡”部分。
    

***

**Step 6: Document and Merge  
第六步：文档并合并**

-   Use the **Generate documentation** smart action to add docstrings to your new algorithmic methods.  
    使用**生成文档**智能作，为你的新算法方法添加文档字符串。
    
-   Update your `README.md` with a short section called **Smarter Scheduling** summarizing your new features.  
    用一个简短的“ **更智能排程** ”栏目更新你的 `README.md`，总结你的新功能。
    
-   Commit and push your changes directly to the `main` branch:  
    提交并直接推送你的更改到`主`分支：
    
    ```
    git add <span>.</span>
    git commit <span>-m</span> <span>"feat: implement sorting, filtering, and conflict detection"</span>
    git push origin main
    ```
    

📍**Checkpoint**: You've added algorithmic intelligence to PawPal+! Your system can now sort, filter, detect conflicts, and handle recurring tasks, all verified through your CLI demo script.  
📍**Checkpoint**：你为 PawPal+添加了算法智能！你的系统现在可以对 CLI 演示脚本进行排序、筛选、检测冲突和处理重复任务。

Phase 5: Testing and Verification  
第五阶段：测试与验证

**⏰ ~30 mins  ⏰ ~30分钟**

In this phase, you'll test and verify that your PawPal+ system works as intended. You'll write and run simple tests to confirm that your classes, algorithms, and scheduling logic behave correctly, and use AI to help generate, explain, and review those tests.  
在此阶段，您将测试并验证您的 PawPal+系统是否按预期运行。你将编写并运行简单的测试，以确认你的课程、算法和调度逻辑是否正确，并利用 AI 帮助生成、解释和审核这些测试。

**Step 1: Plan What to Test  
第一步：规划检测内容**

-   Review your `pawpal_system.py` and list 3–5 core behaviors to verify.  
    回顾你的 `pawpal_system.py`，列出 3 到 5 个核心行为以供核实。
    
-   Start a New Chat Session in Copilot Chat to focus entirely on testing.  
    在 Copilot 聊天中开启一个新的聊天会话，专注于测试。
    
-   Use `#codebase` to ask Copilot for a test plan: "What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" .  
    用 `#codebase` 向 Copilot 询问测试计划：“对于带有分类和重复任务的宠物调度器来说，测试最重要的边缘情况有哪些？”
    
    Focus on "happy paths" (everything works) and "edge cases" (e.g., a pet with no tasks, or two tasks at the exact same time).  
    重点关注“顺利路径”（一切顺利）和“边缘情况”（例如，宠物没有任务，或者同时有两个任务）。
    

***

**Step 2: Build the Automated Test Suite  
步骤2：构建自动化测试套件**

-   Create a new file called `tests/test_pawpal.py`.  
    创建一个名为 `tests/test_pawpal.py` 的新文件。
    
-   Use the **Generate tests** smart action or Copilot Chat to draft your test functions.  
    使用 **“生成测试**智能动作”或 Copilot 聊天来起草你的测试功能。
    
-   Ensure your suite includes at least:  
    确保您的套房至少包含：
    
    -   **Sorting Correctness:** Verify tasks are returned in chronological order.  
        **排序正确性：** 验证任务按时间顺序返回。
        
    -   **Recurrence Logic:** Confirm that marking a daily task complete creates a new task for the following day.  
        **递现逻辑：** 确认标记每日任务完成会为第二天创建一个新任务。
        
    -   **Conflict Detection:** Verify that the `Scheduler` flags duplicate times.  
        **冲突检测：** 确认`调度器`是否标记了重复的时间。
        
        Use **Ask mode** in Chat to explain any test code you don't understand before you save it.  
        在保存之前，使用聊天中的**询问模式**解释你不理解的测试代码。
        
    

***

**Step 3: Run and Debug  
步骤3：运行和调试**

-   In your terminal, run your tests using: `python -m pytest`.  
    在终端里，用 `python -m pytest` 运行测试。
    
-   If a test fails, use **Inline Chat** on the failing test and ask: "Why is this test failing, and is the bug in my test code or my `pawpal_system.py` logic?".  
    如果测试失败，使用在线**聊天**对失败的测试进行询问：“为什么这个测试失败？是我的测试代码出了问题还是 `pawpal_system.py` 逻辑出了问题？”
    
-   Rerun `python -m pytest` until all tests pass with green checkmarks.  
    重复运行 `python -m pytest`，直到所有测试都通过并带有绿色勾选。
    

***

**Step 4: Finalize Documentation and Merge  
步骤4：最终完成文档并合并**

-   Open your `README.md` and add a section titled "Testing PawPal+".  
    打开你的 `README.md`，添加一个名为“测试 PawPal+”的部分。
    
-   Include the command to run tests (`python -m pytest`) and a brief description of what your tests cover.  
    包含运行测试的命令（`python -m pytest`）和测试内容的简要描述。
    
-   Provide your "Confidence Level" (1–5 stars) in the system's reliability based on your test results.  
    根据你的测试结果，给出系统可靠性的“信心等级”（1-5星）。
    
-   Commit and push your test suite to the `main` branch:  
    提交并推送你的测试套件到`主`分支：
    
    ```
    git add <span>.</span>
    git commit <span>-m</span> <span>"test: add automated test suite for PawPal+ system"</span>
    git push origin main
    ```
    

📍**Checkpoint**: You've built a robust test suite that verifies your system's intelligence! You've practiced using AI to generate and debug tests while maintaining the human oversight needed to ensure they are meaningful.  
📍**Checkpoint**：你们构建了一个强大的测试套件，验证系统智能！你练习使用人工智能生成和调试测试，同时保持必要的人工监督以确保测试有意义。

Phase 6: UI Polish, Documentation, and Reflection  
第六阶段：界面润色、文档与反思

**⏰ ~30 mins  ⏰ ~30分钟**

In this final phase, you will package your PawPal+ project for others to understand and use. You'll ensure your UI accurately reflects the smart logic you built, finalize your system diagram, and complete a deep reflection on your AI-assisted engineering process.  
在最后阶段，你将打包你的 PawPal+项目，供他人理解和使用。你将确保用户界面准确反映你构建的智能逻辑，完善系统图，并对 AI 辅助工程流程进行深入反思。

**Step 1: Reflect the Algorithmic Layer in the UI  
步骤1：在用户界面中反映算法层**

Your backend is now "smart," but your UI might still be basic. Ensure the user can actually see and use the features you built in Phase 3.  
你的后端现在是“智能”的，但你的用户界面可能仍然很基础。确保用户能够真正看到并使用你在第三阶段构建的功能。

-   Update your display logic in `app.py` to use the methods from your `Scheduler` class (like sorting or conflict warnings).  
    在 `app.py` 中更新显示逻辑，使用调`度`类的方法（比如排序或冲突警告）。
    
-   Use Streamlit components like `st.success`, `st.warning`, or `st.table` to make the sorted and filtered data look professional.  
    使用 Streamlit 组件，如 `st.success`、`st.warning` 或 `st.table`，使排序和筛选的数据看起来专业。
    
    If your `Scheduler` flags a task conflict, how should that warning be presented in the Streamlit UI to be most helpful to a pet owner?  
    如果你的`调度器`标记了任务冲突，应该如何在 Streamlit 界面中展示这个警告，才能对宠物主人最有帮助？
    

***

**Step 2: Finalize Your System Architecture (UML)  
步骤 2：最终确定你的系统架构（UML）**

-   Revisit the Mermaid.js UML diagram you drafted in Phase 1. Does it still match your final code in `pawpal_system.py`?  
    重新查看你在第一阶段绘制的 Mermaid.js UML 图。它还和你最终的 `pawpal_system.py` 代码匹配吗？
    
-   Use Copilot with `#file:pawpal_system.py` and ask: "Based on my final implementation, what updates should I make to my initial UML diagram to accurately show how my classes interact?".  
    用 Copilot 配合 `#file:pawpal_system.py`，问：“根据我的最终实现，我应该对初始 UML 图做哪些更新，才能准确展示我的类之间的相互作用？”
    
-   Adjust your Mermaid code or draw.io diagram to reflect any new methods or relationships you added during the build.  
    调整你的美人鱼代码或 draw.io 图，以反映你在构建过程中添加的任何新方法或关系。
    
-   Save your final diagram as `uml_final.png` (or a similar image format) in your project folder.  
    把最终的图纸保存为 `uml_final.png`（或类似的图片格式）到你的项目文件夹里。
    

***

**Step 3: Polish Your README  
步骤 3：润色你的 README**

-   Open `README.md`. Your README should act as a professional manual for your app.  
    开`门 README.md`。你的 README 应该作为你应用的专业手册。
    
-   Use Copilot with `#codebase` to help draft a "Features" list that accurately describes the algorithms you implemented (e.g., "Sorting by time," "Conflict warnings," "Daily recurrence").  
    使用 `#codebase` 的 Copilot 帮助起草一个“功能”列表，准确描述你实现的算法（例如，“按时间排序”、“冲突警告”、“每日重复”）。
    
-   Include a screenshot of your final Streamlit app in the "📸 Demo" section.  
    在“📸演示”部分附上你最终的 Streamlit 应用截图。
    
    To embed your screenshot, use the Markdown syntax: `<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>`.  
    要嵌入你的截图，可以使用 Markdown 语法： `<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>` 。
    

***

**Step 4: Write Your Reflection  
第四步：写下你的反思**

-   Open `reflection.md`. You will complete the structured prompts covering your design choices, tradeoffs, and AI strategy.  
    `reflection.md`。你将完成结构化的提示，涵盖你的设计选择、权衡和人工智能策略。
    
-   Reflect on AI Strategy: Specifically describe your experience with VS Code Copilot:  
    反思 AI 战略：具体描述你使用 VS Code Copilot 的体验：
    
    -   Which Copilot features were most effective for building your scheduler?  
        哪些 Copilot 功能在构建调度器时最有效？
    -   Give one example of an AI suggestion you rejected or modified to keep your system design clean.  
        举一个你拒绝或修改过的 AI 建议，以保持系统设计的简洁。
    -   How did using separate chat sessions for different phases help you stay organized?  
        为不同阶段分别使用聊天会话，如何帮助你保持组织有序？
    
-   Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.  
    总结一下你在与强大 AI 工具合作时，作为“首席架构师”的经验。
    

📍**Checkpoint**: You've documented, reflected on, and finalized your PawPal+ project, transforming it from a coding exercise into a polished, professional artifact! You can now clearly explain your design, your reasoning, and your role as the human collaborator in an AI-assisted workflow.  
📍 **检查点** ：你已经记录、反思并完善了你的 PawPal+项目，将其从一个编程练习转变为一个精致、专业的成果！你现在可以清楚地解释你的设计、你的推理，以及你作为 AI 辅助工作流程中人类协作者的角色。

Optional Extensions   可选扩展

**⏰ ~30 mins  ⏰ ~30分钟**

Finished early or want to challenge yourself? Try extending PawPal+ with new features or smarter functionality. Each idea below builds on what you’ve already learned while letting you explore new tools or techniques.  
提前完成了还是想挑战自己？试着用新功能或更智能的功能扩展 PawPal+。以下每个想法都在你已有的基础上建立，同时让你探索新的工具或技术。

-   **Challenge 1: Data Persistence with Agent Mode  
    挑战1：代理模式下的数据持久性**
    
    -   Make your PawPal+ system remember pets and tasks between runs by saving them to a `data.json` file.  
        通过保存到 `data.json` 文件，让你的 PawPal+系统在每次游戏间记住宠物和任务。
        
    -   Use **Agent Mode** to plan and execute the changes. Tell the Agent: "Add `save_to_json` and `load_from_json` methods to the `Owner` class in `#file:pawpal_system.py`, then update the Streamlit state in \`#file:app.py to load this data on startup".  
        使用**代理模式**来规划和执行这些变更。告诉代理：“在 `#file:pawpal_system.py` 的 `Owner` 类中添加 `save_to_json` 和 `load_from_json` 方法，然后在'#file:app.py 中更新 Streamlit 状态，以便在启动时加载这些数据。”
        
        Persistence can be tricky with complex objects. Ask Copilot how to use a library like `marshmallow` or a custom dictionary conversion to handle JSON serialization.  
        对于复杂对象，持久性可能比较棘手。问问 Copilot 如何使用像 `marshmallow` 这样的库或自定义字典转换来处理 JSON 序列化。
        
    
-   **Challenge 2: Advanced Priority Scheduling and UI  
    挑战二：高级优先级调度与用户界面**
    
    -   Go beyond simple time sorting by adding **Priority-Based Scheduling**.  
        通过添加**基于优先级的调度** ，超越简单的时间排序。
    -   Add a "Priority" level (Low, Medium, High) to your `Task` class and update your Scheduler to sort by priority first, then by time.  
        在`任务`类中添加一个“优先级”级别（低、中、高），并更新调度器先按优先级排序，再按时间排序。
    -   Use the **Fix with Copilot** or **Inline Chat** features to add emojis or color-coding to your Streamlit table based on task priority (e.g., 🔴 for High, 🟡 for Medium).  
        使用“**Fix with Copilot**”或 **“Inline Chat**”功能，根据任务优先级（例如🔴高优先级、🟡中级）在 Streamlit 表格中添加表情符号或颜色编码。
    
-   **Challenge 3: Multi-Model Prompt Comparison  
    挑战三：多模型提示比较**
    
    -   Choose a complex algorithmic task (like the logic for rescheduling weekly tasks) and ask for a solution from two different models (e.g., OpenAI vs. Claude or Gemini).  
        选择一个复杂的算法任务（比如每周任务重新安排的逻辑），并从两个不同模型中寻求解答（例如 OpenAI 与 Claude 或 Gemini）。
    -   In your `reflection.md`, add a **Prompt Comparison** section documenting which model provided a more modular or "Pythonic" solution and why.  
        在`你的 reflection.md` 中，添加一个**提示**比较部分，记录哪个模型提供了更模块化或“Python”式的解决方案及其原因。
    

📍**Checkpoint**: You've gone beyond the base requirements and made PawPal+ more capable and professional! These extensions demonstrate your ability to use AI for high-level system planning, data management, and user experience design.  
📍 **检查点** ：你超越了基础要求，让 PawPal+变得更加强大和专业！这些扩展展示了你在高级系统规划、数据管理和用户体验设计中利用人工智能的能力。

### 📬 Submitting Your Project  
📬 提交您的项目

Once you've completed all the required features for your project, use the following checklist to prepare your work for submission.  
完成项目所需的所有功能后，请使用以下清单准备提交作品。

1.  Code is pushed to the correct GitHub repository  
    代码会被推送到正确的 GitHub 仓库
2.  Repo is public  仓库是公开的
3.  Required files are present (code, README, reflection, tests if applicable)  
    必备文件（代码、README、反射文件、测试（如适用）
4.  Commit history shows multiple meaningful commits  
    提交历史显示有多个有意义的提交
5.  Reflection answers the prompts with specific, honest details  
    《反思》用具体且诚实的细节回答了这些提示
6.  Final changes are committed and pushed before the deadline  
    最终修改会在截止日期前提交并推迟
7.  Submit your assignment using the submit button.  
    请通过提交按钮提交您的作业。