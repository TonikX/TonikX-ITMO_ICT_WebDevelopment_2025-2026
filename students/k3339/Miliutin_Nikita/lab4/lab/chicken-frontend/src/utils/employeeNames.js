// src/utils/employeeNames.js

// фиксированные имена под конкретные employee_id
export const EMPLOYEE_NAMES_BY_ID = {
  1: "Иванов Иван Иванович",
  2: "Петров Пётр Петрович",
  3: "Сидорова Анна Сергеевна",
  4: "Кузнецов Дмитрий Олегович",
  5: "Смирнова Мария Андреевна",
  // заранее на будущее:
  6: "Попов Алексей Михайлович",
  7: "Васильева Екатерина Павловна",
};

// запасные ФИО (если появится employee_id, которого нет в словаре)
const FALLBACK_FIOS = [
  "Фёдоров Артём Никитич",
  "Морозова Ольга Викторовна",
];

export function getEmployeeDisplayName(employeeId) {
  const id = Number(employeeId);
  if (!id || Number.isNaN(id)) return "Работник";

  if (EMPLOYEE_NAMES_BY_ID[id]) return EMPLOYEE_NAMES_BY_ID[id];

  // “по кругу” для любых новых работников
  return FALLBACK_FIOS[(id - 1) % FALLBACK_FIOS.length];
}
