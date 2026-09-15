<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Helpdesk Agent - Chat UI</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #16213e;
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #0f3460;
        }
        .header h1 {
            font-size: 1.25rem;
            color: #e94560;
        }
        .version-badge {
            background: #0f3460;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #00d9ff;
        }
        .chat-container {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            padding: 24px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 20px;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user {
            text-align: right;
        }
        .message .role {
            font-size: 0.75rem;
            color: #888;
            margin-bottom: 4px;
        }
        .message.user .role { color: #00d9ff; }
        .message.agent .role { color: #e94560; }
        .message .content {
            background: #16213e;
            padding: 14px 18px;
            border-radius: 12px;
            display: inline-block;
            max-width: 80%;
            line-height: 1.5;
        }
        .message.user .content {
            background: #0f3460;
        }
        .tool-call {
            background: #0d7377;
            padding: 10px 14px;
            border-radius: 8px;
            margin-top: 8px;
            font-family: monospace;
            font-size: 0.85rem;
        }
        .tool-call .tool-name {
            color: #ffd700;
            font-weight: bold;
        }
        .tool-result {
            background: #1a3a3a;
            padding: 10px 14px;
            border-radius: 8px;
            margin-top: 6px;
            font-family: monospace;
            font-size: 0.8rem;
            max-height: 200px;
            overflow-y: auto;
        }
        .input-area {
            background: #16213e;
            padding: 20px 24px;
            border-top: 1px solid #0f3460;
        }
        .input-row {
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            gap: 12px;
        }
        .input-row input {
            flex: 1;
            padding: 14px 18px;
            border: 1px solid #0f3460;
            border-radius: 25px;
            background: #1a1a2e;
            color: #eee;
            font-size: 1rem;
            outline: none;
        }
        .input-row input:focus {
            border-color: #e94560;
        }
        .input-row button {
            padding: 14px 28px;
            background: #e94560;
            border: none;
            border-radius: 25px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .input-row button:hover {
            background: #d63a54;
        }
        .input-row button:disabled {
            background: #555;
            cursor: not-allowed;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #888;
            border-radius: 50%;
            border-top-color: #00d9ff;
            animation: spin 1s linear infinite;
            margin-left: 10px;
            vertical-align: middle;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .history-selector {
            max-width: 900px;
            margin: 0 auto 16px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .history-btn {
            padding: 6px 12px;
            background: #0f3460;
            border: 1px solid #0f3460;
            border-radius: 15px;
            color: #aaa;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .history-btn:hover, .history-btn.active {
            background: #e94560;
            border-color: #e94560;
            color: white;
        }
        .info-panel {
            background: #0d1b2a;
            border: 1px solid #0f3460;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .info-panel h3 {
            color: #e94560;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }
        .info-panel .stats {
            display: flex;
            gap: 24px;
            font-size: 0.85rem;
        }
        .info-panel .stat {
            color: #aaa;
        }
        .info-panel .stat span {
            color: #00d9ff;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 IT Helpdesk Agent</h1>
        <span class="version-badge" id="version">v2</span>
    </div>

    <div class="info-panel">
        <h3>📊 Session Info</h3>
        <div class="stats">
            <div class="stat">Provider: <span id="provider">openrouter</span></div>
            <div class="stat">Model: <span id="model">gpt-4o-mini</span></div>
            <div class="stat">Messages: <span id="msgCount">0</span></div>
        </div>
    </div>

    <div class="history-selector" id="historySelector"></div>

    <div class="chat-container" id="chatContainer"></div>

    <div class="input-area">
        <div class="input-row">
            <input type="text" id="userInput" placeholder="Nhập câu hỏi IT của bạn..." disabled>
            <button id="sendBtn" disabled>Send</button>
        </div>
    </div>

    <script>
        // Sample conversations from eval results
        const sampleConversations = [
            {
                id: "H01",
                title: "VPN Status",
                messages: [
                    { role: "user", content: "Dịch vụ VPN production hiện có đang gặp sự cố không?" },
                    { role: "tool", tool: "check_service_status", args: { service: "vpn", environment: "production" }, result: { status: "degraded", incident: "Intermittent authentication failures" } },
                    { role: "agent", content: "Dịch vụ VPN production hiện đang gặp sự cố. Tình trạng: **degraded**. Vorfall: Intermittent authentication failures for some Windows clients. Vị trí bị ảnh hưởng: Bangkok, Remote. Đã có workaround: Retry once after synchronizing the device clock." }
                ]
            },
            {
                id: "H02",
                title: "Device Check",
                messages: [
                    { role: "user", content: "Kiểm tra tổng thể laptop LT-204 giúp mình." },
                    { role: "tool", tool: "inspect_device", args: { asset_id: "LT-204", check: "all" }, result: { os: "Windows 11 23H2", vpn: "AUTH_TIMEOUT", disk: "healthy" } },
                    { role: "agent", content: "Đã kiểm tra laptop LT-204 (Lenovo ThinkPad T14 Gen 4). Kết quả: VPN client ghi nhận AUTH_TIMEOUT. Disk SMART healthy, endpoint agent healthy. Battery 86%." }
                ]
            },
            {
                id: "H10",
                title: "Missing Asset - Clarify",
                messages: [
                    { role: "user", content: "Kiểm tra Wi-Fi trên laptop của mình giúp nhé." },
                    { role: "tool", tool: "clarify", args: { question: "Bạn cho mình xin mã tài sản (VD: LT-204)?", response_type: "text" }, awaiting: true },
                    { role: "agent", content: "Bạn cho mình xin mã tài sản (VD: LT-204)?" }
                ]
            },
            {
                id: "H12",
                title: "Ticket Confirmation",
                messages: [
                    { role: "user", content: "Tạo ticket mức high cho lỗi VPN trên LT-204 giúp mình." },
                    { role: "tool", tool: "clarify", args: { question: "Tóm tắt ticket: Lỗi VPN trên LT-204, mức ưu tiên: high. Bạn có đồng ý tạo ticket này không?", response_type: "yes_no" }, awaiting: true },
                    { role: "agent", content: "Tóm tắt ticket: Lỗi VPN trên LT-204, mức ưu tiên: high. Bạn có đồng ý tạo ticket này không?" }
                ]
            },
            {
                id: "H13",
                title: "Parallel Tools",
                messages: [
                    { role: "user", content: "VPN trên LT-204 lỗi; kiểm tra cả trạng thái VPN production và máy đó." },
                    { role: "tool", tool: "inspect_device", args: { asset_id: "LT-204", check: "vpn" }, result: { vpn: "AUTH_TIMEOUT" } },
                    { role: "tool", tool: "check_service_status", args: { service: "vpn", environment: "production" }, result: { status: "degraded" } },
                    { role: "agent", content: "Đã kiểm tra cả hai nguồn: Thiết bị LT-204 ghi nhận VPN AUTH_TIMEOUT; Dịch vụ VPN production đang degraded. Đề xuất: Retry sau khi đồng bộ đồng hồ." }
                ]
            }
        ];

        let currentConversation = null;
        let msgCount = 0;

        function renderMessage(msg) {
            const div = document.createElement('div');
            div.className = `message ${msg.role === 'user' ? 'user' : 'agent'}`;

            const roleLabel = msg.role === 'user' ? '👤 Bạn' : msg.role === 'tool' ? '🔧 Tool Call' : '🤖 Agent';
            div.innerHTML = `<div class="role">${roleLabel}</div>`;

            if (msg.role === 'tool') {
                const toolCall = document.createElement('div');
                toolCall.className = 'tool-call';
                toolCall.innerHTML = `<span class="tool-name">${msg.tool}</span>(${JSON.stringify(msg.args)})`;
                div.querySelector('.content') || div.appendChild(document.createElement('div')).className = 'content';
                div.querySelector('.content').appendChild(toolCall);

                if (msg.awaiting) {
                    const awaiting = document.createElement('div');
                    awaiting.style.color = '#ffd700';
                    awaiting.style.marginTop = '8px';
                    awaiting.textContent = '⏳ Đang chờ phản hồi...';
                    div.querySelector('.content').appendChild(awaiting);
                } else if (msg.result) {
                    const result = document.createElement('div');
                    result.className = 'tool-result';
                    result.textContent = JSON.stringify(msg.result, null, 2);
                    div.querySelector('.content').appendChild(result);
                }
            } else {
                const content = document.createElement('div');
                content.className = 'content';
                content.textContent = msg.content;
                div.appendChild(content);
            }

            return div;
        }

        function loadConversation(conv) {
            currentConversation = conv;
            const container = document.getElementById('chatContainer');
            container.innerHTML = '';

            conv.messages.forEach(msg => {
                container.appendChild(renderMessage(msg));
            });

            container.scrollTop = container.scrollHeight;

            // Update history buttons
            document.querySelectorAll('.history-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.id === conv.id);
            });
        }

        function initHistorySelector() {
            const selector = document.getElementById('historySelector');
            sampleConversations.forEach(conv => {
                const btn = document.createElement('button');
                btn.className = 'history-btn';
                btn.dataset.id = conv.id;
                btn.textContent = `${conv.id}: ${conv.title}`;
                btn.onclick = () => loadConversation(conv);
                selector.appendChild(btn);
            });
            loadConversation(sampleConversations[0]);
        }

        // Demo mode - no backend needed
        document.getElementById('userInput').disabled = false;
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('userInput').placeholder = "Demo mode - Select conversation above to view...";

        initHistorySelector();
    </script>
</body>
</html>
