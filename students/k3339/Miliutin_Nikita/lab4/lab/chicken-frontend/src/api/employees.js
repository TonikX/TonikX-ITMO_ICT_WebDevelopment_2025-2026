import { http } from "./http";

export async function getEmployees(params = {}) {
  const res = await http.get("/employees/", { params });
  return res.data;
}

export async function getEmployee(employeeId) {
  const res = await http.get(`/employees/${employeeId}`);
  return res.data;
}

export async function getEmployeeWithAssignments(employeeId) {
  const res = await http.get(`/employees/${employeeId}/assignments`);
  return res.data;
}

// ✅ назначить работника на клетку
// POST /employees/{employee_id}/cages/{cage_id}
// body: { assigned_from: "YYYY-MM-DD", assigned_to?: "YYYY-MM-DD" | null }
export async function assignEmployeeToCage(employeeId, cageId, payload) {
  const res = await http.post(`/employees/${employeeId}/cages/${cageId}`, payload);
  return res.data;
}

// ✅ завершить назначение (закрыть активное)
// PATCH /employees/{employee_id}/cages/{cage_id}
// body: { assigned_to: "YYYY-MM-DD" }
export async function unassignEmployeeFromCage(employeeId, cageId, payload) {
  const res = await http.patch(`/employees/${employeeId}/cages/${cageId}`, payload);
  return res.data;
}

export async function createEmployee(payload) {
  const res = await http.post("/employees/", payload);
  return res.data;
}
