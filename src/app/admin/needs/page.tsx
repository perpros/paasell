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
  { id: 2, name: 'Need 2', status: 'Closed' },
  { id: 3, name: 'Need 3', status: 'Open' },
];

export default function NeedsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Needs
      </Typography>
      <Button variant="contained" color="primary" sx={{ mb: 2 }}>
        Create Need
      </Button>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
