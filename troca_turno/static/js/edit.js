function setAcao(acao) {
    document.getElementById('acao').value = acao;
    document.querySelector('form').submit();
}

function confirmAndSetAcao(acao) {
    var confirmationMessage = "Deseja realmente finalizar a passagem? Não será possível editar após a finalização";
    if (confirm(confirmationMessage)) {
        setAcao(acao);
    }
}