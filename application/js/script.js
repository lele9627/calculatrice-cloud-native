const display = document.getElementById('display');

function appendToDisplay(value) {
    display.value += value;
}

function clearDisplay() {
    display.value = '';
}

async function calculate() {
    const expr = display.value.trim();
    if (!expr) return;

    try {
        const res = await fetch('/api/calc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: expr })
        });

        const data = await res.json();

        if (res.ok) {
            display.value = data.result;
        } else {
            showTempMessage(data.error || 'Erreur');
        }

    } catch {
        showTempMessage('Erreur de connexion');
    }
}

function showTempMessage(message) {
    const original = display.value;
    display.value = message;

    setTimeout(() => {
        display.value = original;
    }, 10000);
}
