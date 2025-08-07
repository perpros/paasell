'use client';

import { useAuth } from '@/hooks/useAuth';
import { UserRole } from '@/types';
import { useRouter } from 'next/navigation';
import { ComponentType, useEffect } from 'react';

const withAuth = <P extends object>(
  WrappedComponent: ComponentType<P>,
  allowedRoles: UserRole[]
) => {
  const AuthComponent = (props: P) => {
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!user) {
        router.push('/'); // Redirect to login page if not authenticated
        return;
      }

      if (!allowedRoles.includes(user.role)) {
        router.push('/'); // Redirect to a "not authorized" page or home
      }
    }, [user, router]);

    if (!user || !allowedRoles.includes(user.role)) {
      return null; // or a loading spinner
    }

    return <WrappedComponent {...props} />;
  };

  return AuthComponent;
};

export default withAuth;
