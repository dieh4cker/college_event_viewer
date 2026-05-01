function showSection(section){
 document.getElementById('studies').classList.add('hidden-s');
 document.getElementById('admission').classList.add('hidden-s');
 document.getElementById(section).classList.remove('hidden-s');
}

function showTrade(trade){
 document.getElementById('tradeContent').classList.remove('hidden-s');
 let title = "";
 let desc = "";

 switch(trade){
 case 'ce': title="Computer Engineering"; desc="Focus on software, coding and systems."; break;
 case 'civil': title="Civil Engineering"; desc="Deals with construction and infrastructure."; break;
 case 'ee': title="Electrical Engineering"; desc="Focus on electrical systems and power."; break;
 case 'me': title="Mechanical Engineering"; desc="Deals with machines and manufacturing."; break;
 case 'it': title="Information Technology"; desc="Focus on IT systems and networking."; break;
 case 'iot': title="Internet of Things"; desc="Smart devices and automation."; break;
 }

 document.getElementById('tradeTitle').innerText = title;
 document.getElementById('tradeDesc').innerText = desc;

 let semDiv = document.getElementById('semesterButtons');
 semDiv.innerHTML = "";
 for(let i=1;i<=6;i++){
 let btn = document.createElement('button');
 btn.innerText = "Semester " + i;
 btn.className = "semester-btn-s";
 btn.onclick = ()=>showSubjects(i);
 semDiv.appendChild(btn);
 }
}

function showSubjects(sem){
 let subDiv = document.getElementById('subjects');
 subDiv.innerHTML = "<h4>Subjects for Semester " + sem + "</h4>";
 for(let i=1;i<=6;i++){
 subDiv.innerHTML += "<p>Subject "+i+"</p>";
 }
}

function showTimetable(sem){
 document.getElementById('timetable').innerHTML = "<h4>Timetable for Semester "+sem+"</h4><p>[Add timetable here]</p>";
}