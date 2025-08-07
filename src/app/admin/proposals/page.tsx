'use client';

import { Table } from '@/components/common/Table';
import { Box, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'need', label: 'Need' },
  { id: 'supplier', label: 'Supplier' },
  { id: 'status', label: 'Status' },
];

const mockData = [
  { id: 1, need: 'Need 1', supplier: 'Supplier A', status: 'Pending' },
  { id: 2, need: 'Need 1', supplier: 'Supplier B', status: 'Accepted' },
  { id: 3, need: 'Need 2', supplier: 'Supplier C', status: 'Rejected' },
];

export default function ProposalsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Proposals
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
