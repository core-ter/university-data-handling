import os
import shutil
from data.solution.generator import generate_people, generate_departments, generate_projects, assign_departments, assign_projects
from data.solution.handler import csv_handler, json_handler, xlsx_handler, sql_handler
from data.solution import extra_pandas

def main():
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Create subdirectories
    csv_dir = os.path.join(output_dir, "csv")
    json_dir = os.path.join(output_dir, "json")
    xlsx_dir = os.path.join(output_dir, "xlsx")
    
    os.makedirs(csv_dir)
    os.makedirs(json_dir)
    os.makedirs(xlsx_dir)

    print("Generating data...")
    people = generate_people(1000)
    departments = generate_departments(10)
    projects = generate_projects(50)
    
    dept_assignments = assign_departments(people, departments)
    proj_assignments = assign_projects(people, projects)

    print(f"Generated {len(people)} people, {len(departments)} departments, {len(projects)} projects.")

    # --- CSV Test ---
    print("\nTesting CSV Handler...")
    csv_handler.write_people(people, csv_dir, file_name="people.csv")
    csv_handler.write_departments(departments, csv_dir)
    csv_handler.write_projects(projects, csv_dir)
    csv_handler.write_dept_assignments(dept_assignments, csv_dir)
    csv_handler.write_proj_assignments(proj_assignments, csv_dir)

    read_people = csv_handler.read_people(csv_dir)
    read_depts = csv_handler.read_departments(csv_dir)
    read_projs = csv_handler.read_projects(csv_dir)
    
    assert len(read_people) == len(people)
    assert len(read_depts) == len(departments)
    assert len(read_projs) == len(projects)
    print("CSV Write/Read successful.")

    # --- JSON Test ---
    print("\nTesting JSON Handler...")
    json_handler.write_departments(departments, json_dir)
    json_handler.write_projects(projects, json_dir)
    
    read_depts_json = json_handler.read_departments(json_dir)
    read_projs_json = json_handler.read_projects(json_dir)
    
    assert len(read_depts_json) == len(departments)
    assert len(read_projs_json) == len(projects)
    print("JSON Write/Read successful.")

    # --- XLSX Test ---
    print("\nTesting XLSX Handler...")
    xlsx_handler.write_departments(departments, xlsx_dir)
    xlsx_handler.write_projects(projects, xlsx_dir)
    
    read_depts_xlsx = xlsx_handler.read_departments(xlsx_dir)
    read_projs_xlsx = xlsx_handler.read_projects(xlsx_dir)
    
    assert len(read_depts_xlsx) == len(departments)
    assert len(read_projs_xlsx) == len(projects)
    print("XLSX Write/Read successful.")

    # --- SQL Test ---
    print("\nTesting SQL Handler...")
    try:
        # Requires VPN and valid credentials
        conn = sql_handler.get_connection()
        print("Connected to Oracle DB.")
        
        sql_handler.create_tables(conn)
        sql_handler.insert_data(conn, people, departments, projects, dept_assignments, proj_assignments)
        sql_handler.read_data(conn)
        
        conn.close()
        print("SQL Write/Read successful.")
    except Exception as e:
        print(f"SQL Test Skipped/Failed: {e}")
        print("Ensure you are on the university network and have set the correct credentials in src/data/solution/handler/sql_handler.py")

    # --- Pandas Extra Test ---
    print("\nGenerating Statistics...")
    extra_pandas.generate_statistics(csv_dir, output_dir)
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    main()
