messages
├── system：Agent 的身份和行为规则
├── user：用户提供的信息和任务
└── assistant：Agent 以前的推理结果或回答

只保存 user 时，Agent 具备的是：记住用户输入

同时保存 user 和 assistant 后，Agent 才具备：记住完整交互过程

以后 Agent 调用搜索、计算器或代码工具时，工具返回的结果也需要进入状态，否则 Agent 下一步就不知道工具刚才返回了什么。

一个完整的Agent状态流程可以理解为：

```
用户输入
   ↓
写入 user 消息
   ↓
模型推理
   ↓
获得 assistant 回复
   ↓
写入 assistant 消息
   ↓
下一轮携带完整历史继续推理
```



Agent 需要一个**记忆管理策略**。现在实现的是最简单的滑动窗口记忆：

```
始终保留 system
+
保留最近 10 轮 user/assistant
+
删除更早的对话
```

