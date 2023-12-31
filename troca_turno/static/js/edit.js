function setAcao(acao) {
    document.getElementById('acao').value = acao;
    document.querySelector('form').submit();
}

function setDtDelete(acao, dt) {
    document.getElementById('acao').value = acao;
    document.getElementById('dt-delete').value = dt;
    document.querySelector('form').submit();
}

function confirmAndSetAcao(acao) {
    let confirmationMessage = "Deseja realmente finalizar a passagem? Não será possível editar após a finalização";
    if (confirm(confirmationMessage)) {
        setAcao(acao);
    }
}

function showPopupAlreadyExists() {
    Toastify({
        text: "DT já adicionada a essa passagem.",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}

function showPopupAdded() {
    Toastify({
        text: "DT adicionada com sucesso!",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#0b9b42"
        }
        }).showToast();
}

function showPopupDoesntExists() {
    Toastify({
        text: "DT inexistente, verifique a digitação.",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}

function showPopupBlank() {
    Toastify({
        text: "O campo não pode estar em branco.",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}

function showPopupDelete() {
    Toastify({
        text: "DT removida com sucesso.",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}

function showPopupUserCreated() {
    Toastify({
        text: "Usuário registrado com sucesso!",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#0b9b42"
        }
        }).showToast();
}

function showPopupFailUserCreated() {
    Toastify({
        text: "Erro ao registrar o usuário, verifique as informações digitadas.",
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}

function showPopupGreen(text) {
    Toastify({
        text: text,
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#0b9b42"
        }
        }).showToast();
}

function showPopupRed(text) {
    Toastify({
        text: text,
        duration: 2000,
        gravity: "top",
        position: "center",
        stopOnFocus: true,
        style: {
        fontSize: "14px",
        height: "auto",
        width: "250px",
        borderRadius: "10px",
        background: "#ba3b3b"
        }
        }).showToast();
}
