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