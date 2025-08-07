'use client';

import { Table } from '@/components/common/Table';
import { Box, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'name', label: 'Name' },
  { id: 'role', label: 'Role' },
];

const mockData = [
  { id: 1, name: 'Admin User', role: 'Admin' },
  { id: 2, name: 'Supplier User', role: 'Supplier' },
  { id: 3, name: 'Distributor User', role: 'Distributor' },
];

export default function UsersPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Users
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
