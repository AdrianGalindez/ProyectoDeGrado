// ===========================MODO OSCURO ===============================
function toggleModoOscuro(){

        const inputModoOscuro = document.getElementById("modoOscuro");
        
        const contenedorChat = document.getElementById("chatContainer");

        const contenedorRespuesta = document.getElementById("respuesta");

        const body = document.querySelector("body");

        const nav = document.querySelector("nav");

        const footer = document.querySelector("footer");



        if (inputModoOscuro.checked){

            body.classList.add("bodyModoOscuro");

            nav.classList.add("NavFooterModoOscuro");

            footer.classList.add("NavFooterModoOscuro");

            contenedorChat.classList.add("chatModoOscuro");

            contenedorRespuesta.classList.add("chatModoOscuro");

            localStorage.setItem("modoOscuro", "true"); // Guardar el estado en localStorage
            
        }else{

            body.classList.remove("bodyModoOscuro");
            
            nav.classList.remove("NavFooterModoOscuro");
            
            footer.classList.remove("NavFooterModoOscuro");

            contenedorChat.classList.remove("chatModoOscuro");

            contenedorRespuesta.classList.remove("chatModoOscuro");

            localStorage.setItem("modoOscuro", "false"); // Guardar el estado en localStorage
        }      

}

document.addEventListener("DOMContentLoaded", function(){
    const modoOscuroGuardado = localStorage.getItem("modoOscuro");
    const inputModoOscuro = document.getElementById("modoOscuro");
    if (modoOscuroGuardado === "true") {
        inputModoOscuro.checked = true;
        toggleModoOscuro();
    }
});



// =======================================================



// ========================= TAMAÑO FUENTE ==================================
function SlideTamañoFuente(valor){
    body = document.querySelector("body");
    body.style.fontSize = valor + "%";
}
// =========================================================================


