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
        // 1) Envoyer le calcul
        const res = await fetch('/api/calc', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: expr })
        });

        const data = await res.json();

        if (!res.ok) {
            showTempMessage(data.error || 'Erreur');
            return;
        }

        const id = data.id;
        display.value = 'Waiting for result…';

        // 2) Polling du résultat
        pollResult(id);

    } catch {
        showTempMessage('Erreur de connexion');
    }
}

async function pollResult(id) {
    try {
        const res = await fetch(`/api/result/${id}`);
        const data = await res.json();

        if (data.status === 'done') {
            display.value = data.result;
            return;
        }

        if (data.status === 'error') {
            showTempMessage(data.error || 'Erreur de calcul');
            return;
        }

        // waiting → on continue à poll
        setTimeout(() => pollResult(id), 500);

    } catch (error) {
        console.error('Erreur polling:', error);
        showTempMessage('Erreur de connexion');
    }
}

function showTempMessage(message) {
    const original = display.value;
    display.value = message;

    setTimeout(() => {
        // Si l'affichage n'a pas changé entre temps, on efface
        if (display.value === message) {
            display.value = '';
        }
    }, 3000);
}
