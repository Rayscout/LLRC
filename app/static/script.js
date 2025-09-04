/*
 LLRC Header Start
 文件功能: 前端 JavaScript 脚本：app/static/script.js
 创建时间: 2025-08-22 12:59
 创建人: 张宇成
 更新记录:
 - 2025-08-22 13:29 by 侯东杨
- 2025-08-29 09:09 by 张宇成
 LLRC Header End
*/
/*
FILE-HEADER-AUTO-ADDED
文件: app/static/script.js
功能: 通用模块
创建时间: 2025-08-26 12:14
创建人: 苏杰
更新记录:
- 2025-08-24 15:21 by 潘显雨
- 2025-08-26 14:41 by 谢佳悦
- 2025-09-01 14:01 by 苏杰
*/
const body = document.querySelector("body"),
      // support old .mode-toggle and new #themeToggle
      modeToggle = body.querySelector(".mode-toggle") || document.getElementById("themeToggle"),
      sidebar = body.querySelector("nav"),
      sidebarToggle = body.querySelector(".sidebar-toggle");

// restore theme
let getMode = localStorage.getItem("mode");
if(getMode === "dark"){ body.classList.add("dark"); }
if(modeToggle){
  // reflect state to checkbox if present
  try { if("checked" in modeToggle) modeToggle.checked = body.classList.contains("dark"); } catch(e){}
}

// restore sidebar status
let getStatus = localStorage.getItem("status");
if(getStatus === "close"){ sidebar && sidebar.classList.add("close"); }

// theme toggle listener (robust)
if(modeToggle){
  const toggleHandler = () => {
    body.classList.toggle("dark");
    const isDark = body.classList.contains("dark");
    localStorage.setItem("mode", isDark ? "dark" : "light");
    try { if("checked" in modeToggle) modeToggle.checked = isDark; } catch(e){}
  };
  modeToggle.addEventListener("click", toggleHandler);
  modeToggle.addEventListener("change", toggleHandler);
}

if(sidebarToggle){
  sidebarToggle.addEventListener("click", () => {
      if(!sidebar) return;
      sidebar.classList.toggle("close");
      localStorage.setItem("status", sidebar.classList.contains("close") ? "close" : "open");
  });
}