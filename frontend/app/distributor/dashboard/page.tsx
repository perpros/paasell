'use client';

import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import Table from '@/components/Table';
import { Typography, CircularProgress, Alert, Button } from '@mui/material';
import { useAuth } from '@/context/AuthContext';
import { useNotification } from '@/context/NotificationContext';

interface Campaign {
  id: number;
  name: string;
  description: string;
  commission_rate: number;
}

const fetchCampaigns = async (token: string | null) => {
  if (!token) {
    throw new Error('No token found');
  }
  const { data } = await api.get<Campaign[]>('/campaigns', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data;
};

export default function DistributorDashboardPage() {
  const { token } = useAuth();
  const { showNotification } = useNotification();
  const { data, error, isLoading } = useQuery<Campaign[], Error>({
    queryKey: ['campaigns', token],
    queryFn: () => fetchCampaigns(token),
    enabled: !!token,
  });

  const handleTestNotification = () => {
    showNotification('This is a test notification!', 'success');
  };

  if (isLoading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error.message}</Alert>;
  }

  const columns = [
    { id: 'name', label: 'Name' },
    { id: 'description', label: 'Description' },
    { id: 'commission_rate', label: 'Commission Rate' },
  ];

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Campaigns
      </Typography>
      <Button onClick={handleTestNotification} variant="contained" sx={{ mb: 2 }}>
        Show Test Notification
      </Button>
      <Table columns={columns} data={data || []} />
    </div>
  );
}
