import pandas as pd
import os
import json

def generate_statistics(input_path: str, output_path: str, output_file: str = "stats.html") -> None:
    """
    Reads CSV files from input_path, calculates statistics, and exports to an interactive HTML report in output_path.
    """
    try:
        # Load data
        people_df = pd.read_csv(os.path.join(input_path, "people.csv"), sep=";")
        depts_df = pd.read_csv(os.path.join(input_path, "departments.csv"), sep=";")
        projects_df = pd.read_csv(os.path.join(input_path, "projects.csv"), sep=";")
        dept_assign_df = pd.read_csv(os.path.join(input_path, "dept_assignments.csv"), sep=";")
        
        # Merge for Department Stats
        people_dept = pd.merge(people_df, dept_assign_df, left_on="id", right_on="person_id")
        people_dept = pd.merge(people_dept, depts_df, left_on="department_id", right_on="id", suffixes=("_person", "_dept"))

        # Prepare data for JavaScript
        # We want a dictionary where keys are Department Names and values are lists of employees
        dept_data = {}
        for dept_name in depts_df["name"].unique():
            dept_employees = people_dept[people_dept["name_dept"] == dept_name]
            employees_list = []
            for _, row in dept_employees.iterrows():
                employees_list.append({
                    "name": row["name_person"],
                    "age": row["age"],
                    "job": row["job"],
                    "salary": row["salary"]
                })
            
            # Calculate dept stats
            avg_age = dept_employees["age"].mean() if not dept_employees.empty else 0
            avg_salary = dept_employees["salary"].mean() if not dept_employees.empty else 0
            
            dept_data[dept_name] = {
                "avg_age": round(avg_age, 1),
                "avg_salary": round(avg_salary, 0),
                "count": len(dept_employees),
                "employees": employees_list
            }

        # Project Stats
        proj_stats = projects_df.agg({"budget": ["sum", "mean", "min", "max"]}).reset_index()
        proj_stats.columns = ["Metric", "Value"]
        proj_stats["Value"] = proj_stats["Value"].round(2)
        proj_html = proj_stats.to_html(index=False, classes="table table-striped")
        
        # Status distribution
        status_counts = projects_df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        status_html = status_counts.to_html(index=False, classes="table table-striped")

        # JSON serialization for JS
        dept_data_json = json.dumps(dept_data)

        # HTML Template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Interactive Project Statistics</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding: 20px; background-color: #f8f9fa; }}
                .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header text-center">
                    <h1>📊 Data Handling Project Statistics</h1>
                    <p class="text-muted">Interactive Report</p>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-primary text-white">Project Overview</div>
                            <div class="card-body">
                                <h5>Budget Metrics</h5>
                                {proj_html}
                                <h5 class="mt-4">Project Status</h5>
                                {status_html}
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-success text-white">Department Explorer</div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <label for="deptSelect" class="form-label">Select Department:</label>
                                    <select class="form-select" id="deptSelect">
                                        <option value="">-- Choose a Department --</option>
                                    </select>
                                </div>
                                
                                <div id="deptStats" style="display:none;">
                                    <div class="row text-center mb-3">
                                        <div class="col-4">
                                            <h6>Employees</h6>
                                            <h4 id="empCount">0</h4>
                                        </div>
                                        <div class="col-4">
                                            <h6>Avg Age</h6>
                                            <h4 id="avgAge">0</h4>
                                        </div>
                                        <div class="col-4">
                                            <h6>Avg Salary</h6>
                                            <h4 id="avgSalary">$0</h4>
                                        </div>
                                    </div>
                                    
                                    <h6>Employee List</h6>
                                    <div style="max-height: 300px; overflow-y: auto;">
                                        <table class="table table-sm table-hover">
                                            <thead>
                                                <tr><th>Name</th><th>Job</th><th>Salary</th></tr>
                                            </thead>
                                            <tbody id="empTableBody">
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const deptData = {dept_data_json};
                const deptSelect = document.getElementById('deptSelect');
                const deptStats = document.getElementById('deptStats');
                const empCount = document.getElementById('empCount');
                const avgAge = document.getElementById('avgAge');
                const avgSalary = document.getElementById('avgSalary');
                const empTableBody = document.getElementById('empTableBody');

                // Populate Dropdown
                Object.keys(deptData).sort().forEach(dept => {{
                    const option = document.createElement('option');
                    option.value = dept;
                    option.textContent = dept;
                    deptSelect.appendChild(option);
                }});

                // Handle Change
                deptSelect.addEventListener('change', function() {{
                    const selected = this.value;
                    if (!selected) {{
                        deptStats.style.display = 'none';
                        return;
                    }}

                    const data = deptData[selected];
                    deptStats.style.display = 'block';
                    
                    empCount.textContent = data.count;
                    avgAge.textContent = data.avg_age;
                    avgSalary.textContent = '$' + data.avg_salary.toLocaleString();

                    // Populate Table
                    empTableBody.innerHTML = '';
                    data.employees.forEach(emp => {{
                        const row = `<tr>
                            <td>${{emp.name}}</td>
                            <td>${{emp.job}}</td>
                            <td>$${{emp.salary.toLocaleString()}}</td>
                        </tr>`;
                        empTableBody.innerHTML += row;
                    }});
                }});
            </script>
        </body>
        </html>
        """

        with open(os.path.join(output_path, output_file), "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Interactive statistics generated successfully: {os.path.join(output_path, output_file)}")

    except Exception as e:
        print(f"Error generating statistics: {e}")
        import traceback
        traceback.print_exc()
