function setExample(text) {
    document.getElementById("question").value = text;
}

function askQuestion() {
    const question = document
        .getElementById("question")
        .value
        .trim();

    const result = document.getElementById("result");

    result.className = "result";

    // Case 1: Người dùng chưa nhập gì
    if (question === "") {
        result.classList.add("error");

        result.innerHTML = `
            <strong>Bạn chưa nhập câu hỏi.</strong>
            <p>Hãy nhập một câu hỏi về bài học của khóa AI20k.</p>
        `;

        return;
    }

    const lowerQuestion = question.toLowerCase();

    // Case 2: Câu hỏi quá mơ hồ
    if (
        lowerQuestion === "cái này là sao?" ||
        lowerQuestion === "cái này là gì?" ||
        lowerQuestion === "giải thích đi" ||
        question.length < 10
    ) {
        result.classList.add("warning");

        result.innerHTML = `
            <strong>Mình chưa đủ thông tin để trả lời.</strong>

            <p>
                Bạn đang hỏi về bài học hoặc chủ đề nào?
            </p>

            <p>
                Ví dụ: "ReAct Agent là gì?"
            </p>
        `;

        return;
    }

    // Case 3: Demo happy path
    if (
        lowerQuestion.includes("react") ||
        lowerQuestion.includes("agent")
    ) {
        result.classList.add("success");

        result.innerHTML = `
            <strong>ReAct Agent</strong>

            <p>
                ReAct là cách xây dựng agent bằng cách luân phiên
                giữa suy luận và hành động.
            </p>

            <p>
                Agent có thể suy nghĩ về bước tiếp theo,
                gọi công cụ nếu cần, quan sát kết quả rồi tiếp tục.
            </p>

            <div class="source">
                <strong>Nguồn tham khảo:</strong><br>
                Day 3 - ReAct Agent
            </div>

            <p>
                ⚠️ CP2: kết quả hiện tại là dữ liệu mock,
                chưa phải câu trả lời từ AI thật.
            </p>
        `;

        return;
    }

    // Case 4: Không có căn cứ
    result.classList.add("warning");

    result.innerHTML = `
        <strong>Mình chưa tìm thấy căn cứ phù hợp.</strong>

        <p>
            Thay vì đoán câu trả lời, bạn có thể nói rõ
            tên bài học hoặc chủ đề muốn hỏi.
        </p>

        <p>
            Ví dụ: "Trong Day 3, ReAct Agent hoạt động như thế nào?"
        </p>
    `;
}