const file=document.getElementById("file"), preview=document.getElementById("preview"), empty=document.getElementById("empty"), detect=document.getElementById("detect"), loading=document.getElementById("loading"), drop=document.getElementById("drop");

function useFile(f){
 if(!f || !f.type.startsWith("image/")) return alert("Please select an image.");
 if(f.size>5*1024*1024) return alert("Maximum file size is 5MB.");
 const reader=new FileReader();
 reader.onload=e=>{preview.src=e.target.result;preview.style.display="block";empty.style.display="none";detect.disabled=false;detect.classList.add("ready")};
 reader.readAsDataURL(f);
}
file.onchange=()=>useFile(file.files[0]);
["dragover","dragenter"].forEach(x=>drop.addEventListener(x,e=>{e.preventDefault();drop.style.borderColor="#9cff32"}));
drop.addEventListener("drop",e=>{e.preventDefault();drop.style.borderColor="";useFile(e.dataTransfer.files[0])});
document.getElementById("camera").onclick=()=>file.click();

detect.onclick=async()=>{
 if(!file.files[0]) return;
 const fd=new FormData();fd.append("image",file.files[0]);
 detect.disabled=true;detect.querySelector("span").textContent="Analyzing...";loading.style.display="block";
 try{
  const r=await fetch("/detect",{method:"POST",body:fd}), data=await r.json();
  if(!r.ok) throw Error(data.error);
  const a=Number(data.absorption), d=Number(data.dry);
  document.getElementById("percent").textContent=a.toFixed(1)+"%";
  document.getElementById("absorbed").textContent=a.toFixed(1)+"%";
  document.getElementById("dry").textContent=d.toFixed(1)+"%";
  document.getElementById("ring").style.background=`conic-gradient(#45e99a 0 ${a}%,#29323d ${a}% 100%)`;
  document.getElementById("insight").textContent=data.insight;
 }catch(e){alert(e.message||"Detection failed")}
 detect.disabled=false;detect.querySelector("span").textContent="Analysis Complete";loading.style.display="none";
};

document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{
 document.querySelectorAll(".page").forEach(p=>p.classList.add("hidden"));
 document.getElementById(b.dataset.page).classList.remove("hidden");
 document.querySelectorAll("nav button").forEach(n=>n.classList.remove("active"));b.classList.add("active");
});
document.getElementById("theme").onclick=()=>alert("Dark mode is the official IdlySambarAI mode. 🌙");
