function setExample(text) {
    document.getElementById("question").value = text;
}

function getApiUrl() {
    if (window.location.protocol === "file:") {
        return "http://127.0.0.1:5000/api/ask";
    }

    return "/api/ask";
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function setResult(type, html) {
    const result = document.getElementById("result");
    result.className = `result ${type}`;
    result.innerHTML = html;
}

function renderSources(sourceIds) {
    if (!sourceIds || sourceIds.length === 0) {
        return "";
    }

    const items = sourceIds
        .map((sourceId) => `<li>${escapeHtml(sourceId)}</li>`)
        .join("");

    return `
        <div class="source">
            <strong>Nguồn tham khảo:</strong>
            <ul>${items}</ul>
        </div>
    `;
}

function renderDecision(data) {
    const decision = data.decision;
    const answer = escapeHtml(data.answer || "");
    const reason = escapeHtml(data.reason || "");

    if (decision === "ANSWER") {
        setResult(
            "success",
            `
                <strong>AI trả lời có căn cứ</strong>
                <p>${answer}</p>
                ${renderSources(data.source_ids)}
                <p class="reason">Lý do quyết định: ${reason}</p>
            `
        );
        return;
    }

    if (decision === "CLARIFY") {
        setResult(
            "warning",
            `
                <strong>AI cần bạn làm rõ</strong>
                <p>${answer}</p>
                <p class="reason">Lý do quyết định: ${reason}</p>
            `
        );
        return;
    }

    if (decision === "OUT_OF_SCOPE") {
        setResult(
            "warning",
            `
                <strong>AI không tìm thấy căn cứ phù hợp</strong>
                <p>${answer}</p>
                <p class="reason">Lý do quyết định: ${reason}</p>
            `
        );
        return;
    }

    setResult(
        "error",
        `
            <strong>Chưa thể xử lý phản hồi</strong>
            <p>${answer || "Backend chưa trả về decision hợp lệ."}</p>
        `
    );
}

async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    const sendButton = document.getElementById("sendButton");

    if (question === "") {
        setResult(
            "error",
            `
                <strong>Bạn chưa nhập câu hỏi.</strong>
                <p>Hãy nhập một câu hỏi về bài học của khóa AI20k.</p>
            `
        );
        return;
    }

    sendButton.disabled = true;
    sendButton.textContent = "Đang gọi AI...";
    setResult(
        "loading",
        `
            <strong>Đang gửi tới backend</strong>
            <p>Backend sẽ gọi Gemini để quyết định ANSWER / CLARIFY / OUT_OF_SCOPE.</p>
        `
    );

    try {
        const response = await fetch(getApiUrl(), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        if (!response.ok) {
            setResult(
                "error",
                `
                    <strong>Chưa gọi được AI</strong>
                    <p>${escapeHtml(data.answer || data.error || "Backend trả lỗi.")}</p>
                `
            );
            return;
        }

        renderDecision(data);
    } catch (error) {
        setResult(
            "error",
            `
                <strong>Không kết nối được backend</strong>
                <p>Hãy chạy <code>python codebase/server.py</code> rồi thử lại.</p>
            `
        );
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Gửi câu hỏi";
    }
}
