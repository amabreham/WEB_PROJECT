const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
 const manageUser=document.getElementById('manage_user')
const manageDrug=document.getElementById('manage_drug')
const sendReport=document.getElementById('send_report')
const viewReport=document.getElementById('view_report')
// side btns
const user_btn=document.getElementById('user_btn')
const drug_btn=document.getElementById('drug_btn')
const send_report=document.getElementById('send_report_btn')
const view_report=document.getElementById('view_report_btn')
allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', ()=> {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});
  
	user_btn.addEventListener("click", ()=> {
 		if (manageUser.classList.contains("hidden")) {
		  manageUser.classList.remove("hidden");
		  manageDrug.classList.add("hidden");
		  viewReport.classList.add("hidden");
		  sendReport.classList.add("hidden");

 		}  
	  });
	  console.log(drug_btn.classList)
	drug_btn.addEventListener("click", ()=> {
 		if (manageDrug.classList.contains("hidden")) {
			manageDrug.classList.remove("hidden");
			manageUser.classList.add("hidden");
			viewReport.classList.add("hidden");
			sendReport.classList.add("hidden");

 		}  
	  });
 
	send_report.addEventListener("click", ()=> {
 		if (sendReport.classList.contains("hidden")) {
			sendReport.classList.remove("hidden");
			viewReport.classList.add("hidden");
			manageDrug.classList.add("hidden");
			manageUser.classList.add("hidden");
 		}  
	  });
	view_report.addEventListener("click", ()=> {
 		if (viewReport.classList.contains("hidden")) {
			viewReport.classList.remove("hidden");
			manageUser.classList.add("hidden");
			manageDrug.classList.add("hidden");
			sendReport.classList.add("hidden");
 		}  
	  });
 


 


// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})