// ====================================VERIFICAR RESPUESTA CORRECTA=========================================
const respuestas= document.querySelectorAll(".respuesta_correcta"); // Obtener el contenedor de respuesta correcta

const boton_verificar= document.getElementById("verificar"); // obtener el boton de verificar respuestas 

document.addEventListener("DOMContentLoaded",function(){

for(let i=0; i<totalDePreguntas;i++){
   const radio = document.querySelector(`input[name="opciones_${id}"]:checked`)
   if(radio){
       console.log(`=== pregunta ${i} == respuesta === ${radio.value}`);
   }else{
       console.log(`pregunta ${i} sin respuesta`);
   }
}
})



boton_verificar.addEventListener("click",function(){   // funcion para ocultar respuestas 
    
    respuestas.forEach(respuesta => {
         respuesta.classList.toggle("ocultar_respuesta");
    });
       
})




// =========================================================================================