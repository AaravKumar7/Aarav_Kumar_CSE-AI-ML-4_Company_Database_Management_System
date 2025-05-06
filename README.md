# Aarav_Kumar_CSE-AI-ML-4_Company_Database_Management_System
I built a full-stack web app using Django with JWT authentication for secure login and user access. It has a clean API setup and connects smoothly with the frontend, making the experience dynamic and user-friendly. It’s designed to be scalable and works great for things like dashboards or portals.
# Django JWT Auth Web App

A simple full-stack web app using Django REST Framework with JWT authentication and frontend integration.

## Video explanation
Company_database_management_system_GpNo16_B.mp4

## Features
- User registration & login
- JWT-based authentication
- RESTful APIs
- Frontend integration

## How to Run

1. Clone the repo and navigate to it  
2. Create and activate a virtual environment  
3. Run: `pip install -r requirements.txt`  
4. Run migrations: `python manage.py migrate`  
5. Create superuser (optional): `python manage.py createsuperuser`  
6. Start server: `python manage.py runserver`

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Company Management Dashboard</title>
    <style>
        body { font-family: ""Arial, sans-serif; margin: 0; padding: 0;  background-color:aliceblue; }
        .navbar { background: #007BFF; color: #fff; text-align: center; padding: 15px; font-size: 24px; }
        .sidebar { width: 200px; background: #f8f8f8; position: fixed; height: 100%; padding-top: 20px; display: none; }
        .sidebar a { padding: 15px; display: block; color: #007BFF; cursor: pointer; }
        .sidebar a:hover { background: #e8e8e8; }
        .content { margin-left: 210px; padding: 20px; }
        .section { display: none; }
        .section.active { display: block; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid black; padding: 10px; }
        th { background-color: #007BFF; color: white; }
        input, button { padding: 8px; margin: 5px; }
    </style>
</head>
<body onload="forceLogin()">
<div class="navbar">Company Dashboard</div>
<div class="sidebar" id="sidebar">
    <a onclick="showSection('dashboard')">Dashboard</a>
    <a onclick="showSection('employees')">Employees</a>
    <a onclick="showSection('machines')">Machines</a>
    <a onclick="showSection('projects')">Projects</a>
    <a onclick="showSection('vehicles')">Vehicles</a>
    <a onclick="logout()">Logout</a>
</div>
<div class="content">
    <div id="loginSection" class="section active">
        <h2>Login</h2>
        <input type="text" id="username" placeholder="Username">
        <input type="password" id="password" placeholder="Password">
        <button onclick="login()">Login</button>
    </div>
    <div id="dashboard" class="section">
        <h2>Dashboard</h2>
        <p>Employees: <span id="empCount">0</span></p>
        <p>Machines: <span id="machineCount">0</span></p>
        <p>Projects: <span id="projectCount">0</span></p>
        <p>Vehicles: <span id="vehicleCount">0</span></p>
    </div>
    <div id="employees" class="section">
        <h2>Employee Management</h2>
        <div id="empForm"></div>
        <button onclick="addRow('emp')">Add Employee</button>
        <table id="empTable"><thead><tr id="empHeader"></tr></thead><tbody></tbody></table>
        <input id="empNewColumn" placeholder="New Column Name">
        <button onclick="addColumn('emp')">Add Column</button>
        <input id="empRemoveColumn" placeholder="Column Name to Remove">
        <button onclick="removeColumn('emp')">Remove Column</button>
    </div>
    <div id="machines" class="section">
        <h2>Machinery Management</h2>
        <div id="machineForm"></div>
        <button onclick="addRow('machine')">Add Machine</button>
        <table id="machineTable"><thead><tr id="machineHeader"></tr></thead><tbody></tbody></table>
        <input id="machineNewColumn" placeholder="New Column Name">
        <button onclick="addColumn('machine')">Add Column</button>
        <input id="machineRemoveColumn" placeholder="Column Name to Remove">
        <button onclick="removeColumn('machine')">Remove Column</button>
    </div>
    <div id="projects" class="section">
        <h2>Projects Management</h2>
        <div id="projectForm"></div>
        <button onclick="addRow('project')">Add Project</button>
        <table id="projectTable"><thead><tr id="projectHeader"></tr></thead><tbody></tbody></table>
        <input id="projectNewColumn" placeholder="New Column Name">
        <button onclick="addColumn('project')">Add Column</button>
        <input id="projectRemoveColumn" placeholder="Column Name to Remove">
        <button onclick="removeColumn('project')">Remove Column</button>
    </div>
    <div id="vehicles" class="section">
        <h2>Vehicle Management</h2>
        <div id="vehicleForm"></div>
        <button onclick="addRow('vehicle')">Add Vehicle</button>
        <table id="vehicleTable"><thead><tr id="vehicleHeader"></tr></thead><tbody></tbody></table>
        <input id="vehicleNewColumn" placeholder="New Column Name">
        <button onclick="addColumn('vehicle')">Add Column</button>
        <input id="vehicleRemoveColumn" placeholder="Column Name to Remove">
        <button onclick="removeColumn('vehicle')">Remove Column</button>
    </div>
</div>
<script>
let data = { emp: [], machine: [], project: [], vehicle: [] };
let columns = {
    emp: ["Name", "Role", "Contact", "Salary"],
    machine: ["Name", "Type", "Purchase Date", "Maintenance"],
    project: ["Project", "Client", "Budget", "Deadline"],
    vehicle: ["Vehicle Name", "Reg No", "Date of Purchase", "Insurance", "Pollution", "Car Number", "Machine", "Coordinator"]};
function forceLogin() { showSection('loginSection'); }
function login() { 
    let username = document.getElementById('username').value.trim();
    let password = document.getElementById('password').value.trim();
    if (username === "admin" && password === "1234") {
        document.getElementById('sidebar').style.display = 'block'; 
        showSection('dashboard');
    } else {
        alert("Invalid credentials! Username: admin, Password: 1234");
    }
}

function logout() { location.reload(); }
function showSection(id) { document.querySelectorAll('.section').forEach(s => s.classList.remove('active')); document.getElementById(id).classList.add('active'); renderAll(); }
function renderAll() { ['emp', 'machine', 'project', 'vehicle'].forEach(renderSection); }
function renderSection(type) { renderForm(type); renderTable(type); }
function renderForm(type) { document.getElementById(type + 'Form').innerHTML = columns[type].map(c => `<input id="${type}_${c}" placeholder="${c}">`).join(''); }
function renderTable(type) { document.getElementById(type + 'Header').innerHTML = columns[type].map(c => `<th>${c}</th>`).join('') + '<th>Actions</th>'; document.getElementById(type + 'Table').querySelector('tbody').innerHTML = data[type].map((r, i) => `<tr>${columns[type].map(c => `<td contenteditable onblur="updateCell('${type}', ${i}, '${c}', this.innerText)">${r[c] || ''}</td>`).join('')}<td><button onclick="deleteRow('${type}', ${i})">Delete</button></td></tr>`).join(''); }
function addRow(type) { data[type].push(Object.fromEntries(columns[type].map(c => [c, document.getElementById(`${type}_${c}`).value]))); renderTable(type); }
function updateCell(type, i, col, val) { data[type][i][col] = val; }
function deleteRow(type, i) { data[type].splice(i, 1); renderTable(type); }
function addColumn(type) { columns[type].push(prompt('Column Name')); renderAll(); }
function removeColumn(type) {
    const col = document.getElementById(type + 'RemoveColumn').value.trim();
    if (col && columns[type].includes(col)) {
        columns[type] = columns[type].filter(c => c !== col);
        data[type].forEach(row => delete row[col]);
        renderAll();
    } else {
        alert('Column not found!');
    }
}
</script>
</body>
</html>
