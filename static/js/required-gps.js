// EcoTech 1.2.3 - Recursos de localização
function EcoTechGPS(targetId){
 if(!navigator.geolocation){
   alert('Seu navegador não suporta localização.');
   return;
 }
 navigator.geolocation.getCurrentPosition(function(position){
  const field=document.getElementById(targetId);
  if(field){
    field.value='Latitude: '+position.coords.latitude.toFixed(6)+' | Longitude: '+position.coords.longitude.toFixed(6);
  }
 }, function(){
   alert('Não foi possível obter sua localização. Permita o acesso ao GPS.');
 });
}
