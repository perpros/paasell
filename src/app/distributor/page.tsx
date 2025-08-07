'use client';

import withAuth from '@/components/withAuth';

function DistributorPage() {
  return <h1>Distributor Dashboard</h1>;
}

export default withAuth(DistributorPage, ['Distributor']);
