import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Rating
} from '@mui/material';

interface ImageItem {
  id: string;
  src: string;
  title: string;
  category: string;
  rating: number;
  description: string;
}

const ImageGallery: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<ImageItem | null>(null);
  const [open, setOpen] = useState(false);

  // Available images with metadata
  const images: ImageItem[] = [
    {
      id: 'image1',
      src: '/images/image1.jfif.jpeg',
      title: 'AI Dashboard Concept',
      category: 'Dashboard',
      rating: 4.5,
      description: 'Modern AI-powered dashboard interface design'
    },
    {
      id: 'image2',
      src: '/images/image2.jpeg',
      title: 'Schedule Planning',
      category: 'Scheduling',
      rating: 4.8,
      description: 'Intelligent schedule planning and organization'
    },
    {
      id: 'image3',
      src: '/images/image3.jpeg',
      title: 'Progress Tracking',
      category: 'Analytics',
      rating: 4.6,
      description: 'Visual progress tracking and goal monitoring'
    },
    {
      id: 'image4',
      src: '/images/image4.jpeg',
      title: 'Personal Assistant',
      category: 'AI Assistant',
      rating: 4.7,
      description: 'AI personal assistant interaction design'
    },
    {
      id: 'image7',
      src: '/images/image7.jpeg',
      title: 'Data Visualization',
      category: 'Analytics',
      rating: 4.4,
      description: 'Advanced data visualization and insights'
    },
    {
      id: 'image8',
      src: '/images/image8.jpeg',
      title: 'Mobile Interface',
      category: 'Mobile',
      rating: 4.3,
      description: 'Mobile-first design approach'
    },
    {
      id: 'image9',
      src: '/images/image9.jpeg',
      title: 'Calendar Integration',
      category: 'Calendar',
      rating: 4.5,
      description: 'Seamless calendar integration features'
    },
    {
      id: 'image10',
      src: '/images/image10.jpeg',
      title: 'Goal Setting',
      category: 'Goals',
      rating: 4.6,
      description: 'Intuitive goal setting and tracking'
    },
    {
      id: 'image11',
      src: '/images/image11.jpeg',
      title: 'Notification System',
      category: 'Notifications',
      rating: 4.2,
      description: 'Smart notification and reminder system'
    },
    {
      id: 'image12',
      src: '/images/image12.jpeg',
      title: 'User Profile',
      category: 'Profile',
      rating: 4.1,
      description: 'Personalized user profile management'
    }
  ];

  // Sort images by rating (best first)
  const sortedImages = [...images].sort((a, b) => b.rating - a.rating);
  const bestImages = sortedImages.slice(0, 6); // Top 6 images

  const handleImageClick = (image: ImageItem) => {
    setSelectedImage(image);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedImage(null);
  };

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      'Dashboard': '#2196f3',
      'Scheduling': '#4caf50',
      'Analytics': '#ff9800',
      'AI Assistant': '#9c27b0',
      'Mobile': '#f44336',
      'Calendar': '#00bcd4',
      'Goals': '#8bc34a',
      'Notifications': '#ff5722',
      'Profile': '#607d8b'
    };
    return colors[category] || '#757575';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Visionary Design Gallery
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Explore the visual concepts and design inspirations for our AI Personal Scheduler
      </Typography>

      {/* Best Images Section */}
      <Box mb={4}>
        <Typography variant="h5" gutterBottom>
          🏆 Best Rated Designs
        </Typography>
        <Grid container spacing={3}>
          {bestImages.map((image) => (
            <Grid item xs={12} sm={6} md={4} key={image.id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
                onClick={() => handleImageClick(image)}
              >
                <CardMedia
                  component="img"
                  height="200"
                  image={image.src}
                  alt={image.title}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="h6" component="h3">
                      {image.title}
                    </Typography>
                    <Rating value={image.rating} precision={0.1} size="small" readOnly />
                  </Box>
                  <Chip 
                    label={image.category}
                    size="small"
                    sx={{ 
                      backgroundColor: getCategoryColor(image.category),
                      color: 'white',
                      mb: 1
                    }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    {image.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* All Images Section */}
      <Box>
        <Typography variant="h5" gutterBottom>
          📸 Complete Gallery
        </Typography>
        <Grid container spacing={2}>
          {sortedImages.map((image) => (
            <Grid item xs={6} sm={4} md={3} key={image.id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { opacity: 0.8 }
                }}
                onClick={() => handleImageClick(image)}
              >
                <CardMedia
                  component="img"
                  height="120"
                  image={image.src}
                  alt={image.title}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ p: 1 }}>
                  <Typography variant="caption" display="block">
                    {image.title}
                  </Typography>
                  <Rating value={image.rating} precision={0.1} size="small" readOnly />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Image Detail Dialog */}
      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        {selectedImage && (
          <>
            <DialogTitle>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h5">{selectedImage.title}</Typography>
                <Chip 
                  label={selectedImage.category}
                  sx={{ 
                    backgroundColor: getCategoryColor(selectedImage.category),
                    color: 'white'
                  }}
                />
              </Box>
            </DialogTitle>
            <DialogContent>
              <Box textAlign="center" mb={2}>
                <img 
                  src={selectedImage.src}
                  alt={selectedImage.title}
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '400px',
                    objectFit: 'contain'
                  }}
                />
              </Box>
              <Box display="flex" alignItems="center" gap={2} mb={2}>
                <Typography variant="body1">Rating:</Typography>
                <Rating value={selectedImage.rating} precision={0.1} readOnly />
                <Typography variant="body2" color="text.secondary">
                  ({selectedImage.rating}/5.0)
                </Typography>
              </Box>
              <Typography variant="body1">
                {selectedImage.description}
              </Typography>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose}>Close</Button>
              <Button variant="contained" onClick={handleClose}>
                Use This Design
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default ImageGallery;