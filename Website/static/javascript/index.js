async function question() {
    const chatInput = document.getElementById('chat').value;
    if (chatInput.trim() === "") return;

    document.getElementById('chat').value = "";
    const chatBox = document.getElementById('chat-box');
    const spinner = document.getElementById('spinner');
    
    chatBox.style.display = 'block';

    const questionElement = document.createElement('div');
    questionElement.className = 'message question';
    questionElement.innerText = chatInput;
    chatBox.appendChild(questionElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    spinner.style.display = 'block';

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: chatInput })
        });

        const data = await response.json();

        spinner.style.display = 'none';

    
        const responseElement = document.createElement('div');
        responseElement.className = 'message response';
        responseElement.innerText = data.response;
        chatBox.appendChild(responseElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error('Error fetching response:', error);

        spinner.style.display = 'none';

        const errorElement = document.createElement('div');
        errorElement.className = 'message response';
        errorElement.innerText = 'Sorry, there was an error processing your request.';
        chatBox.appendChild(errorElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
