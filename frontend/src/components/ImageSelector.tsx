import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Button,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  Divider,
  Rating,
  Checkbox,
  FormControlLabel,
  Alert,
  LinearProgress
} from '@mui/material';
import BlendIcon from '@mui/icons-material/Blend';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import CompareIcon from '@mui/icons-material/Compare';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { imageAnalyzer } from '../utils/imageAnalyzer';

interface ImageData {
  id: string;
  src: string;
  title: string;
  category: string;
  rating: number;
  useCase: string[];
  colors: string[];
}

const ImageSelector: React.FC = () => {
  const [selectedImages, setSelectedImages] = useState<string[]>([]);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [filterUseCase, setFilterUseCase] = useState<string>('all');
  const [blendMode, setBlendMode] = useState<string>('complete');
  const [analysis, setAnalysis] = useState<any>(null);

  const images = imageAnalyzer.getAllImages();
  const categories = ['all', ...Array.from(new Set(images.map(img => img.category)))];
  const useCases = ['all', ...Array.from(new Set(images.flatMap(img => img.useCase)))];

  useEffect(() => {
    if (selectedImages.length > 0) {
      const newAnalysis = imageAnalyzer.analyzeSelection(selectedImages);
      setAnalysis(newAnalysis);
    } else {
      setAnalysis(null);
    }
  }, [selectedImages]);

  const filteredImages = images.filter(img => {
    const categoryMatch = filterCategory === 'all' || img.category === filterCategory;
    const useCaseMatch = filterUseCase === 'all' || img.useCase.includes(filterUseCase);
    return categoryMatch && useCaseMatch;
  });

  const handleImageSelect = (imageId: string) => {
    setSelectedImages(prev => 
      prev.includes(imageId) 
        ? prev.filter(id => id !== imageId)
        : [...prev, imageId]
    );
  };

  const getRecommendedBlend = () => {
    if (selectedImages.length === 0) return null;

    const selected = images.filter(img => selectedImages.includes(img.id));
    const avgRating = selected.reduce((sum, img) => sum + img.rating, 0) / selected.length;
    const categories = Array.from(new Set(selected.map(img => img.category)));
    const useCases = Array.from(new Set(selected.flatMap(img => img.useCase)));

    return {
      count: selected.length,
      avgRating: avgRating.toFixed(1),
      categories: categories.join(', '),
      useCases: useCases.slice(0, 3).join(', '),
      recommendation: avgRating > 4.5 ? 'Excellent choice!' : avgRating > 4.0 ? 'Good selection' : 'Consider higher rated images'
    };
  };

  const getTopRatedImages = (count: number = 3) => {
    return [...images]
      .sort((a, b) => b.rating - a.rating)
      .slice(0, count)
      .map(img => img.id);
  };

  const getBestForUseCase = (useCase: string, count: number = 2) => {
    return images
      .filter(img => img.useCase.includes(useCase))
      .sort((a, b) => b.rating - a.rating)
      .slice(0, count)
      .map(img => img.id);
  };

  const applyAutoSelection = () => {
    switch (blendMode) {
      case 'best-rated':
        setSelectedImages(getTopRatedImages(4));
        break;
      case 'dashboard-focus':
        setSelectedImages([
          ...getBestForUseCase('dashboard', 2),
          ...getBestForUseCase('overview', 1),
          ...getBestForUseCase('main-interface', 1)
        ]);
        break;
      case 'analytics-focus':
        setSelectedImages([
          ...getBestForUseCase('analytics', 2),
          ...getBestForUseCase('charts', 1),
          ...getBestForUseCase('progress', 1)
        ]);
        break;
      case 'mobile-first':
        setSelectedImages([
          ...getBestForUseCase('mobile', 2),
          ...getBestForUseCase('responsive', 1),
          ...getBestForUseCase('touch', 1)
        ]);
        break;
      default:
        setSelectedImages(getTopRatedImages(3));
    }
  };

  const blend = getRecommendedBlend();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🎨 Image Selector & Blender
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Select and blend the best images for your Visionary application
      </Typography>

      {/* Controls */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                label="Category"
              >
                {categories.map(cat => (
                  <MenuItem key={cat} value={cat}>
                    {cat === 'all' ? 'All Categories' : cat}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Use Case</InputLabel>
              <Select
                value={filterUseCase}
                onChange={(e) => setFilterUseCase(e.target.value)}
                label="Use Case"
              >
                {useCases.map(useCase => (
                  <MenuItem key={useCase} value={useCase}>
                    {useCase === 'all' ? 'All Use Cases' : useCase}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Auto Selection</InputLabel>
              <Select
                value={blendMode}
                onChange={(e) => setBlendMode(e.target.value)}
                label="Auto Selection"
              >
                <MenuItem value="best-rated">Best Rated</MenuItem>
                <MenuItem value="dashboard-focus">Dashboard Focus</MenuItem>
                <MenuItem value="analytics-focus">Analytics Focus</MenuItem>
                <MenuItem value="mobile-first">Mobile First</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={3}>
            <Button
              variant="contained"
              startIcon={<AutoAwesomeIcon />}
              onClick={applyAutoSelection}
              fullWidth
            >
              Auto Select
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Selection Summary */}
      {blend && (
        <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.50' }}>
          <Typography variant="h6" gutterBottom>
            📊 Selection Analysis
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} sm={3}>
              <Typography variant="body2" color="text.secondary">Images Selected</Typography>
              <Typography variant="h6">{blend.count}</Typography>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Typography variant="body2" color="text.secondary">Avg Rating</Typography>
              <Typography variant="h6">{blend.avgRating}/5.0</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">Categories</Typography>
              <Typography variant="body1">{blend.categories}</Typography>
            </Grid>
          </Grid>
          <Box mt={2}>
            <Chip 
              label={blend.recommendation}
              color={blend.avgRating > '4.5' ? 'success' : blend.avgRating > '4.0' ? 'warning' : 'default'}
              icon={<AutoAwesomeIcon />}
            />
          </Box>
        </Paper>
      )}

      {/* Image Grid */}
      <Grid container spacing={2}>
        {filteredImages.map((image) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={image.id}>
            <Card 
              sx={{ 
                cursor: 'pointer',
                border: selectedImages.includes(image.id) ? 2 : 0,
                borderColor: 'primary.main',
                transition: 'all 0.2s'
              }}
            >
              <Box position="relative">
                <CardMedia
                  component="img"
                  height="160"
                  image={image.src}
                  alt={image.title}
                  sx={{ objectFit: 'cover' }}
                />
                <Box position="absolute" top={8} right={8}>
                  <Checkbox
                    checked={selectedImages.includes(image.id)}
                    onChange={() => handleImageSelect(image.id)}
                    sx={{ 
                      bgcolor: 'rgba(255,255,255,0.8)',
                      borderRadius: 1
                    }}
                  />
                </Box>
                <Box position="absolute" top={8} left={8}>
                  <Rating value={image.rating} precision={0.1} size="small" readOnly />
                </Box>
              </Box>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  {image.title}
                </Typography>
                <Box display="flex" gap={0.5} flexWrap="wrap" mb={1}>
                  {image.useCase.slice(0, 2).map(useCase => (
                    <Chip key={useCase} label={useCase} size="small" variant="outlined" />
                  ))}
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {image.category} • {image.rating}/5.0
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Action Buttons */}
      {selectedImages.length > 0 && (
        <Box mt={4} display="flex" gap={2} justifyContent="center">
          <Button
            variant="contained"
            startIcon={<BlendIcon />}
            size="large"
          >
            Create Blend ({selectedImages.length} images)
          </Button>
          <Button
            variant="outlined"
            startIcon={<CompareIcon />}
            size="large"
          >
            Compare Selected
          </Button>
          <Button
            variant="text"
            onClick={() => setSelectedImages([])}
            size="large"
          >
            Clear Selection
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default ImageSelector;