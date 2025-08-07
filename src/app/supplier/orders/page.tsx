'use client';

import { Table } from '@/components/common/Table';
import { Box, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'campaign', label: 'Campaign' },
  { id: 'status', label: 'Status' },
];

const mockData = [
  { id: 1, campaign: 'Campaign 1', status: 'Delivered' },
  { id: 2, campaign: 'Campaign 2', status: 'Shipped' },
];

export default function OrdersPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Orders
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
