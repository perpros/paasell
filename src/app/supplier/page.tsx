'use client';

import withAuth from '@/components/withAuth';

function SupplierPage() {
  return <h1>Supplier Dashboard</h1>;
}

export default withAuth(SupplierPage, ['Supplier']);
