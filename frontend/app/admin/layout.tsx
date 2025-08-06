'use client';

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { user, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (token === null || user === null) {
      // still loading
      return;
    }
    if (!token || !user) {
      router.push('/login');
    } else if (user.role !== 'admin') {
      router.push('/'); // Or a not-authorized page
    }
  }, [user, token, router]);

  if (!token || !user || user.role !== 'admin') {
    return null; // Or a loading spinner
  }

  return <>{children}</>;
}
