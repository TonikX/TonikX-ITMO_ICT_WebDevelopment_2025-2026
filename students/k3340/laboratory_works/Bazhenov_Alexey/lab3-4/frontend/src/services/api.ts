import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

import type {
  CleaningAssignment,
  Client,
  Employee,
  FreeRoomsSummary,
  QuarterlyReport,
  Room,
  RoomStay,
  Stay,
} from '../types';

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api';

interface PaginatedResponse<T> {
  results?: T[];
  next?: string | null;
  previous?: string | null;
}

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl,
  }),
  tagTypes: ['Rooms', 'Clients', 'Employees', 'Stays', 'Reports'],
  endpoints: (builder) => ({
    getRooms: builder.query<Room[], { room_type?: string; floor?: number } | void>({
      query: (params) => ({
        url: '/rooms/',
        params: params ?? undefined,
      }),
      providesTags: ['Rooms'],
    }),
    getFreeRooms: builder.query<FreeRoomsSummary, void>({
      query: () => '/rooms/free-count/',
      providesTags: ['Rooms'],
    }),
    getRoomClients: builder.query<
      RoomStay[],
      { roomId: number; start: string; end: string }
    >({
      query: ({ roomId, start, end }) => ({
        url: `/rooms/${roomId}/clients/`,
        params: { start, end },
      }),
      providesTags: ['Stays'],
    }),
    getClients: builder.query<Client[], { city?: string } | void>({
      query: (params) => ({
        url: '/clients/',
        params: params ?? undefined,
      }),
      providesTags: ['Clients'],
      transformResponse: (response: PaginatedResponse<Client> | Client[]) => {
        if (Array.isArray(response)) {
          return response;
        }
        return response.results ?? [];
      },
    }),
    getStays: builder.query<Stay[], { status?: string } | void>({
      query: (params) => ({
        url: '/stays/',
        params: params ?? undefined,
      }),
      providesTags: ['Stays'],
    }),
    createClient: builder.mutation<Client, Partial<Client>>({
      query: (body) => ({
        url: '/clients/',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Clients'],
    }),
    getClientStays: builder.query<Stay[], number>({
      query: (clientId) => `/clients/${clientId}/stays/`,
      providesTags: ['Stays'],
    }),
    getOverlappingClients: builder.query<
      Client[],
      { clientId: number; start: string; end: string }
    >({
      query: ({ clientId, start, end }) => ({
        url: `/clients/${clientId}/overlaps/`,
        params: { start, end },
      }),
    }),
    createStay: builder.mutation<Stay, Partial<Stay>>({
      query: (body) => ({
        url: '/stays/',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Stays', 'Rooms'],
    }),
    checkoutStay: builder.mutation<
      Stay,
      { stayId: number; check_out: string }
    >({
      query: ({ stayId, check_out }) => ({
        url: `/stays/${stayId}/checkout/`,
        method: 'POST',
        body: { check_out },
      }),
      invalidatesTags: ['Stays', 'Rooms', 'Reports'],
    }),
    getEmployees: builder.query<Employee[], void>({
      query: () => '/employees/',
      providesTags: ['Employees'],
    }),
    createEmployee: builder.mutation<Employee, Partial<Employee>>({
      query: (body) => ({
        url: '/employees/',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Employees'],
    }),
    fireEmployee: builder.mutation<Employee, number>({
      query: (employeeId) => ({
        url: `/employees/${employeeId}/fire/`,
        method: 'POST',
      }),
      invalidatesTags: ['Employees'],
    }),
    updateSchedule: builder.mutation<
      Employee,
      { employeeId: number; assignments: CleaningAssignment[] }
    >({
      query: ({ employeeId, assignments }) => ({
        url: `/employees/${employeeId}/schedule/`,
        method: 'PUT',
        body: { assignments },
      }),
      invalidatesTags: ['Employees'],
    }),
    whoCleans: builder.query<
      Employee,
      { clientId: number; weekday: string }
    >({
      query: ({ clientId, weekday }) => ({
        url: '/employees/who-cleans/',
        params: { client_id: clientId, weekday },
      }),
    }),
    getQuarterlyReport: builder.query<
      QuarterlyReport,
      { quarter: number; year: number }
    >({
      query: ({ quarter, year }) => ({
        url: '/reports/quarterly/',
        params: { quarter, year },
      }),
      providesTags: ['Reports'],
    }),
  }),
});

export const {
  useGetRoomsQuery,
  useGetFreeRoomsQuery,
  useGetRoomClientsQuery,
  useGetClientsQuery,
  useGetStaysQuery,
  useCreateClientMutation,
  useGetClientStaysQuery,
  useGetOverlappingClientsQuery,
  useCreateStayMutation,
  useCheckoutStayMutation,
  useGetEmployeesQuery,
  useCreateEmployeeMutation,
  useFireEmployeeMutation,
  useUpdateScheduleMutation,
  useWhoCleansQuery,
  useGetQuarterlyReportQuery,
} = api;

