'use client';

import { Table } from '@/components/common/Table';
import { Box, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'name', label: 'Name' },
  { id: 'status', label: 'Status' },
];

const mockData = [
  { id: 1, name: 'Campaign 1', status: 'Active' },
  { id: 2, name: 'Campaign 2', status: 'Inactive' },
  { id: 3, name: 'Campaign 3', status: 'Active' },
];

export default function CampaignsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Campaigns
      </Typography>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
