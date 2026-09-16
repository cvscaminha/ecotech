document.addEventListener('DOMContentLoaded', function(){
 const cep=document.getElementById('id_cep');
 const address=document.getElementById('id_address');
 const neighborhood=document.getElementById('id_neighborhood');
 const city=document.getElementById('id_city');
 const state=document.getElementById('id_state');
 const cpf=document.getElementById('id_cpf_cnpj');
 const phone=document.getElementById('id_phone');

 function onlyNumbers(v){return (v||'').replace(/\D/g,'');}
 function maskCep(v){v=onlyNumbers(v).slice(0,8); return v.length>5?v.slice(0,5)+'-'+v.slice(5):v;}
 function maskCpf(v){
   v=onlyNumbers(v).slice(0,14);
   if(v.length>11){
     if(v.length>12) return v.slice(0,2)+'.'+v.slice(2,5)+'.'+v.slice(5,8)+'/'+v.slice(8,12)+'-'+v.slice(12);
     return v;
   }
   if(v.length>9) return v.slice(0,3)+'.'+v.slice(3,6)+'.'+v.slice(6,9)+'-'+v.slice(9);
   if(v.length>6) return v.slice(0,3)+'.'+v.slice(3,6)+'.'+v.slice(6);
   if(v.length>3) return v.slice(0,3)+'.'+v.slice(3);
   return v;
 }
 function maskPhone(v){
   v=onlyNumbers(v).slice(0,11);
   if(v.length<=2) return v ? '('+v : v;
   if(v.length<=7) return '('+v.slice(0,2)+') '+v.slice(2);
   return '('+v.slice(0,2)+') '+v.slice(2,7)+'-'+v.slice(7);
 }

 if(cep){
   cep.value=maskCep(cep.value);
   cep.addEventListener('input',()=>cep.value=maskCep(cep.value));
   cep.addEventListener('blur',()=>{
     let value=onlyNumbers(cep.value);
     if(value.length!==8)return;
     fetch('https://viacep.com.br/ws/'+value+'/json/')
      .then(r=>r.json()).then(d=>{
        if(d.erro)return;
        if(address) address.value=d.logradouro||'';
        if(neighborhood) neighborhood.value=d.bairro||'';
        if(city) city.value=d.localidade||'';
        if(state) state.value=d.uf||'';
      });
   });
 }
 if(cpf){ cpf.value=maskCpf(cpf.value); cpf.addEventListener('input',()=>cpf.value=maskCpf(cpf.value)); }
 if(phone){ phone.value=maskPhone(phone.value); phone.addEventListener('input',()=>phone.value=maskPhone(phone.value)); }

 // evita exibição de dois asteriscos provenientes de labels customizados
 document.querySelectorAll('label').forEach(l=>{l.innerHTML=l.innerHTML.replace(/\s\*\s\*/g,' *');});

 // Carregamento de cidades conforme UF selecionada
 if(state && city){
   async function loadCities(uf){
     if(!uf)return;
     try{
       const r=await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados/'+uf+'/municipios');
       const cities=await r.json();
       const current = city.dataset.selectedCity || city.value || city.getAttribute('data-initial-city') || '';
       city.innerHTML='';
       const placeholder=document.createElement('option');
       placeholder.value='';
       placeholder.textContent='Selecione a cidade';
       city.appendChild(placeholder);
       cities.forEach(c=>{
         const option=document.createElement('option');
         option.value=c.nome;
         option.textContent=c.nome;
         city.appendChild(option);
       });
       if(current && [...city.options].some(o=>o.value===current)){
         city.value=current;
       }
       city.dataset.selectedCity = city.value;
     }catch(e){console.error('Erro ao carregar cidades',e);}
   }
   city.addEventListener('change',()=>{
     city.dataset.selectedCity = city.value;
   });
   state.addEventListener('change',()=>{
     // ao trocar UF, a cidade anterior deixa de ser válida
     city.dataset.selectedCity = '';
     loadCities(state.value);
   });
   if(city.value) city.dataset.selectedCity = city.value;
   if(state.value) loadCities(state.value);
 }
});
