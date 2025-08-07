'use client';

import { useAuth } from '@/hooks/useAuth';
import { UserRole } from '@/types';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = (role: UserRole) => {
    login(role);
    if (role) {
      router.push(`/${role.toLowerCase()}`);
    }
  };

  return (
    <div>
      <h1>Login as:</h1>
      <button onClick={() => handleLogin('Admin')}>Admin</button>
      <button onClick={() => handleLogin('Supplier')}>Supplier</button>
      <button onClick={() => handleLogin('Distributor')}>Distributor</button>
    </div>
  );
}
