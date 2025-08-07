'use client';

import { Table } from '@/components/common/Table';
import { Box, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'description', label: 'Description' },
  { id: 'amount', label: 'Amount' },
];

const mockData = [
  { id: 1, description: 'Campaign 1 Payout', amount: '$1000' },
  { id: 2, description: 'Campaign 2 Payout', amount: '$2500' },
  { id: 3, description: 'Platform Fee', amount: '-$500' },
];

export default function FinancesPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Finances
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
