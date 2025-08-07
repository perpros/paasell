'use client';

import { Table } from '@/components/common/Table';
import { useNotify } from '@/hooks/useNotify';
import { Box, Button, Typography } from '@mui/material';

const columns = [
  { id: 'id', label: 'ID' },
  { id: 'name', label: 'Name' },
  { id: 'actions', label: 'Actions' },
];

const mockData = [
  { id: 1, name: 'Campaign 1' },
  { id: 2, name: 'Campaign 2' },
  { id: 3, name: 'Campaign 3' },
];

export default function CampaignsPage() {
  const notify = useNotify();

  const handleGetLink = (campaignId: number) => {
    notify.success(`Link for campaign ${campaignId} generated successfully!`);
  };

  const dataWithActions = mockData.map((row) => ({
    ...row,
    actions: (
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleGetLink(row.id)}
      >
        Get Link
      </Button>
    ),
  }));

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Available Campaigns
      </Typography>
      <Table columns={columns} data={dataWithActions} />
    </Box>
  );
}
