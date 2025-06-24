document.addEventListener("DOMContentLoaded",function(){function e(){let e=document.getElementById("titleInput")?.value||"",t=document.getElementById("dueDateInput")?.value||"",n=document.getElementById("labelsInput")?.value||"",l=document.getElementById("bodyText")?.value||"";document.getElementById("logPreview").innerHTML=`
        <h4><b>${e||""}</b></h4>
        <p><strong></strong> ${t||""}</p>
        <p><strong></strong> ${n||""}</p>
        <p><strong></strong> ${l||""}</p>
    `}["titleInput","dueDateInput","labelsInput","bodyText"].forEach(t=>{let n=document.getElementById(t);n&&n.addEventListener("input",e)}),e()});