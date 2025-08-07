export type UserRole = 'Admin' | 'Supplier' | 'Distributor' | null;

export interface User {
  name: string;
  role: UserRole;
}
