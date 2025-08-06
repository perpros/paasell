'use client';

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DistributorLayout({ children }: { children: React.ReactNode }) {
  const { user, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (token === null || user === null) {
      // still loading
      return;
    }
    if (!token || !user) {
      router.push('/login');
    } else if (user.role !== 'distributor') {
      router.push('/'); // Or a not-authorized page
    }
  }, [user, token, router]);

  if (!token || !user || user.role !== 'distributor') {
    return null; // Or a loading spinner
  }

  return <>{children}</>;
}
