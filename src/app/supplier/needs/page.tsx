'use client';

import { Table } from '@/components/common/Table';
import { Box, Button, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'name', label: 'Name' },
  { id: 'status', label: 'Status' },
];

const mockData = [
  { id: 1, name: 'Need 1', status: 'Open' },
  { id: 3, name: 'Need 3', status: 'Open' },
];

export default function NeedsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Available Needs
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
