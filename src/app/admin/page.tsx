'use client';

import withAuth from '@/components/withAuth';

function AdminPage() {
  return <h1>Admin Dashboard</h1>;
}

export default withAuth(AdminPage, ['Admin']);
