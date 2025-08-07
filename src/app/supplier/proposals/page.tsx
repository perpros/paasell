'use client';

import { Table } from '@/components/common/Table';
import { Box, Button, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'need', label: 'Need' },
  { id: 'status', label: 'Status' },
];

const mockData = [
  { id: 1, need: 'Need 1', status: 'Pending' },
  { id: 2, need: 'Need 1', status: 'Accepted' },
];

export default function ProposalsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Proposals
      </Typography>
      <Button variant="contained" color="primary" sx={{ mb: 2 }}>
        Submit Proposal
      </Button>
      <Table columns={columns} data={mockData} />
    </Box>
  );
}
