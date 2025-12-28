"""
Performance Optimization and Component Cleanup
Task 15.1: Implement systematic component cleanup and optimization
Requirements: 9.1, 9.2
"""

import os
import sys
import json
import logging
import asyncio
import shutil
import time
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import aiofiles
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class OptimizationType(Enum):
    """Types of optimization operations"""
    FILE_CLEANUP = "file_cleanup"
    CACHE_OPTIMIZATION = "cache_optimization"
    DATABASE_OPTIMIZATION = "database_optimization"
    MEMORY_OPTIMIZATION = "memory_optimization"
    NETWORK_OPTIMIZATION = "network_optimization"

@dataclass
class OptimizationResult:
    """Result of optimization operation"""
    optimization_type: OptimizationType
    files_processed: int
    space_freed: int  # bytes
    time_taken: float  # seconds
    errors: List[str]
    details: Dict[str, Any]

class UnusedComponentDetector:
    """Detect and catalog unused components"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.used_files = set()
        self.unused_files = set()
        self.dependency_graph = {}
        
    async def scan_project_structure(self) -> Dict[str, Any]:
        """Scan entire project to identify used and unused components"""
        
        logger.info("Starting project structure scan...")
        start_time = time.time()
        
        # Scan all directories
        all_files = set()
        for root, dirs, files in os.walk(self.project_root):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {
                '.git', '__pycache__', 'node_modules', '.pytest_cache',
                '.hypothesis', '.vscode', 'dist', 'build'
            }]
            
            for file in files:
                file_path = Path(root) / file
                all_files.add(file_path)
        
        # Analyze file dependencies
        await self._analyze_dependencies(all_files)
        
        # Identify unused files
        self.unused_files = all_files - self.used_files
        
        scan_time = time.time() - start_time
        
        return {
            'total_files': len(all_files),
            'used_files': len(self.used_files),
            'unused_files': len(self.unused_files),
            'scan_time': scan_time,
            'unused_file_list': [str(f) for f in self.unused_files]
        }
        
    async def _analyze_dependencies(self, all_files: Set[Path]):
        """Analyze file dependencies to determine usage"""
        
        # Start with entry points
        entry_points = self._find_entry_points(all_files)
        self.used_files.update(entry_points)
        
        # Recursively find dependencies
        to_process = list(entry_points)
        processed = set()
        
        while to_process:
            current_file = to_process.pop(0)
            if current_file in processed:
                continue
                
            processed.add(current_file)
            dependencies = await self._find_file_dependencies(current_file, all_files)
            
            for dep in dependencies:
                if dep not in self.used_files:
                    self.used_files.add(dep)
                    to_process.append(dep)
                    
            self.dependency_graph[str(current_file)] = [str(d) for d in dependencies]
            
    def _find_entry_points(self, all_files: Set[Path]) -> Set[Path]:
        """Find entry point files (main.py, app.py, etc.)"""
        entry_points = set()
        
        entry_patterns = {
            'main.py', 'app.py', 'server.py', 'run.py',
            'index.js', 'index.ts', 'App.js', 'App.tsx',
            'package.json', 'requirements.txt', 'Dockerfile',
            'docker-compose.yml'
        }
        
        for file_path in all_files:
            if file_path.name in entry_patterns:
                entry_points.add(file_path)
                
            # Configuration files
            if file_path.suffix in {'.json', '.yml', '.yaml', '.toml', '.ini'}:
                if any(keyword in file_path.name.lower() for keyword in ['config', 'settings']):
                    entry_points.add(file_path)
                    
        return entry_points
        
    async def _find_file_dependencies(self, file_path: Path, all_files: Set[Path]) -> Set[Path]:
        """Find dependencies for a specific file"""
        dependencies = set()
        
        if not file_path.exists():
            return dependencies
            
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = await f.read()
                
            # Python imports
            if file_path.suffix == '.py':
                dependencies.update(self._find_python_dependencies(content, all_files))
                
            # JavaScript/TypeScript imports
            elif file_path.suffix in {'.js', '.ts', '.jsx', '.tsx'}:
                dependencies.update(self._find_js_dependencies(content, all_files))
                
            # CSS imports
            elif file_path.suffix in {'.css', '.scss', '.sass'}:
                dependencies.update(self._find_css_dependencies(content, all_files))
                
            # Configuration file references
            elif file_path.suffix in {'.json', '.yml', '.yaml'}:
                dependencies.update(self._find_config_dependencies(content, all_files))
                
        except Exception as e:
            logger.warning(f"Error analyzing dependencies for {file_path}: {e}")
            
        return dependencies
        
    def _find_python_dependencies(self, content: str, all_files: Set[Path]) -> Set[Path]:
        """Find Python import dependencies"""
        dependencies = set()
        
        import re
        
        # Find import statements
        import_patterns = [
            r'from\s+(\S+)\s+import',
            r'import\s+(\S+)',
            r'__import__\([\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Convert module name to file path
                module_parts = match.split('.')
                for file_path in all_files:
                    if file_path.suffix == '.py':
                        if file_path.stem in module_parts or file_path.name in module_parts:
                            dependencies.add(file_path)
                            
        return dependencies
        
    def _find_js_dependencies(self, content: str, all_files: Set[Path]) -> Set[Path]:
        """Find JavaScript/TypeScript import dependencies"""
        dependencies = set()
        
        import re
        
        # Find import/require statements
        import_patterns = [
            r'import.*from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import\([\'"]([^\'"]+)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Resolve relative imports
                if match.startswith('./') or match.startswith('../'):
                    # Handle relative paths
                    for file_path in all_files:
                        if match.replace('./', '').replace('../', '') in str(file_path):
                            dependencies.add(file_path)
                else:
                    # Handle absolute imports
                    for file_path in all_files:
                        if match in str(file_path):
                            dependencies.add(file_path)
                            
        return dependencies
        
    def _find_css_dependencies(self, content: str, all_files: Set[Path]) -> Set[Path]:
        """Find CSS import dependencies"""
        dependencies = set()
        
        import re
        
        # Find @import statements
        import_pattern = r'@import\s+[\'"]([^\'"]+)[\'"]'
        matches = re.findall(import_pattern, content)
        
        for match in matches:
            for file_path in all_files:
                if match in str(file_path) or file_path.name == match:
                    dependencies.add(file_path)
                    
        return dependencies
        
    def _find_config_dependencies(self, content: str, all_files: Set[Path]) -> Set[Path]:
        """Find configuration file dependencies"""
        dependencies = set()
        
        try:
            # Parse JSON/YAML content
            if content.strip().startswith('{'):
                config_data = json.loads(content)
            else:
                # Simple YAML parsing for file references
                import re
                file_refs = re.findall(r'[\'"]([^\'"]*/[^\'"]*\.[a-zA-Z0-9]+)[\'"]', content)
                for ref in file_refs:
                    for file_path in all_files:
                        if ref in str(file_path):
                            dependencies.add(file_path)
                            
        except Exception:
            pass
            
        return dependencies

class PerformanceOptimizer:
    """Comprehensive performance optimization system"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.detector = UnusedComponentDetector(project_root)
        self.optimization_history = []
        
    async def run_comprehensive_optimization(self) -> Dict[str, Any]:
        """Run all optimization procedures"""
        
        logger.info("Starting comprehensive performance optimization...")
        start_time = time.time()
        
        results = {}
        
        # 1. Detect unused components
        logger.info("Phase 1: Detecting unused components...")
        scan_result = await self.detector.scan_project_structure()
        results['component_scan'] = scan_result
        
        # 2. File system cleanup
        logger.info("Phase 2: File system cleanup...")
        cleanup_result = await self._optimize_file_system()
        results['file_cleanup'] = cleanup_result
        
        # 3. Cache optimization
        logger.info("Phase 3: Cache optimization...")
        cache_result = await self._optimize_caches()
        results['cache_optimization'] = cache_result
        
        # 4. Database optimization
        logger.info("Phase 4: Database optimization...")
        db_result = await self._optimize_database()
        results['database_optimization'] = db_result
        
        # 5. Memory optimization
        logger.info("Phase 5: Memory optimization...")
        memory_result = await self._optimize_memory()
        results['memory_optimization'] = memory_result
        
        # 6. Network optimization
        logger.info("Phase 6: Network optimization...")
        network_result = await self._optimize_network()
        results['network_optimization'] = network_result
        
        total_time = time.time() - start_time
        
        # Calculate total impact
        total_space_freed = sum(
            result.get('space_freed', 0) 
            for result in results.values() 
            if isinstance(result, dict)
        )
        
        optimization_summary = {
            'total_time': total_time,
            'total_space_freed': total_space_freed,
            'optimizations_performed': len(results),
            'timestamp': datetime.utcnow().isoformat(),
            'results': results
        }
        
        self.optimization_history.append(optimization_summary)
        
        logger.info(f"Optimization completed in {total_time:.2f}s, freed {total_space_freed} bytes")
        
        return optimization_summary
        
    async def _optimize_file_system(self) -> OptimizationResult:
        """Optimize file system by removing unused files"""
        
        start_time = time.time()
        files_processed = 0
        space_freed = 0
        errors = []
        
        # Get unused files from detector
        unused_files = self.detector.unused_files
        
        # Safe file extensions to delete
        safe_extensions = {'.tmp', '.log', '.cache', '.bak', '.old', '.temp'}
        
        for file_path in unused_files:
            try:
                # Only delete files with safe extensions or in temp directories
                if (file_path.suffix in safe_extensions or 
                    'temp' in str(file_path).lower() or
                    'cache' in str(file_path).lower()):
                    
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        space_freed += file_size
                        files_processed += 1
                        
            except Exception as e:
                errors.append(f"Error deleting {file_path}: {e}")
                
        # Clean up empty directories
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):  # Empty directory
                        dir_path.rmdir()
                        files_processed += 1
                except Exception as e:
                    errors.append(f"Error removing empty directory {dir_path}: {e}")
                    
        time_taken = time.time() - start_time
        
        return OptimizationResult(
            optimization_type=OptimizationType.FILE_CLEANUP,
            files_processed=files_processed,
            space_freed=space_freed,
            time_taken=time_taken,
            errors=errors,
            details={'unused_files_found': len(unused_files)}
        )
        
    async def _optimize_caches(self) -> OptimizationResult:
        """Optimize various cache systems"""
        
        start_time = time.time()
        files_processed = 0
        space_freed = 0
        errors = []
        
        # Cache directories to clean
        cache_dirs = [
            self.project_root / '__pycache__',
            self.project_root / '.pytest_cache',
            self.project_root / '.hypothesis',
            self.project_root / 'node_modules' / '.cache',
            self.project_root / 'backend' / '__pycache__',
            self.project_root / 'web_app' / 'node_modules' / '.cache',
            self.project_root / 'mobile_app' / 'node_modules' / '.cache'
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                try:
                    # Calculate size before deletion
                    dir_size = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
                    
                    # Remove cache directory
                    shutil.rmtree(cache_dir)
                    space_freed += dir_size
                    files_processed += 1
                    
                except Exception as e:
                    errors.append(f"Error cleaning cache {cache_dir}: {e}")
                    
        # Clean up log files older than 7 days
        log_cutoff = datetime.now() - timedelta(days=7)
        
        for log_file in self.project_root.rglob('*.log'):
            try:
                if datetime.fromtimestamp(log_file.stat().st_mtime) < log_cutoff:
                    file_size = log_file.stat().st_size
                    log_file.unlink()
                    space_freed += file_size
                    files_processed += 1
                    
            except Exception as e:
                errors.append(f"Error cleaning log file {log_file}: {e}")
                
        time_taken = time.time() - start_time
        
        return OptimizationResult(
            optimization_type=OptimizationType.CACHE_OPTIMIZATION,
            files_processed=files_processed,
            space_freed=space_freed,
            time_taken=time_taken,
            errors=errors,
            details={'cache_dirs_cleaned': len([d for d in cache_dirs if d.exists()])}
        )
        
    async def _optimize_database(self) -> OptimizationResult:
        """Optimize database performance"""
        
        start_time = time.time()
        files_processed = 0
        space_freed = 0
        errors = []
        
        try:
            # Find database files
            db_files = list(self.project_root.rglob('*.db')) + list(self.project_root.rglob('*.sqlite'))
            
            for db_file in db_files:
                try:
                    # Simple database optimization (VACUUM for SQLite)
                    if db_file.suffix in {'.db', '.sqlite'}:
                        import sqlite3
                        
                        original_size = db_file.stat().st_size
                        
                        conn = sqlite3.connect(str(db_file))
                        conn.execute('VACUUM')
                        conn.close()
                        
                        new_size = db_file.stat().st_size
                        space_freed += max(0, original_size - new_size)
                        files_processed += 1
                        
                except Exception as e:
                    errors.append(f"Error optimizing database {db_file}: {e}")
                    
        except Exception as e:
            errors.append(f"Database optimization error: {e}")
            
        time_taken = time.time() - start_time
        
        return OptimizationResult(
            optimization_type=OptimizationType.DATABASE_OPTIMIZATION,
            files_processed=files_processed,
            space_freed=space_freed,
            time_taken=time_taken,
            errors=errors,
            details={'databases_found': len(db_files) if 'db_files' in locals() else 0}
        )
        
    async def _optimize_memory(self) -> OptimizationResult:
        """Optimize memory usage"""
        
        start_time = time.time()
        errors = []
        
        try:
            # Get current memory usage
            process = psutil.Process()
            memory_before = process.memory_info().rss
            
            # Force garbage collection
            import gc
            collected = gc.collect()
            
            # Get memory usage after cleanup
            memory_after = process.memory_info().rss
            memory_freed = max(0, memory_before - memory_after)
            
            time_taken = time.time() - start_time
            
            return OptimizationResult(
                optimization_type=OptimizationType.MEMORY_OPTIMIZATION,
                files_processed=1,
                space_freed=memory_freed,
                time_taken=time_taken,
                errors=errors,
                details={
                    'memory_before': memory_before,
                    'memory_after': memory_after,
                    'objects_collected': collected
                }
            )
            
        except Exception as e:
            errors.append(f"Memory optimization error: {e}")
            
            return OptimizationResult(
                optimization_type=OptimizationType.MEMORY_OPTIMIZATION,
                files_processed=0,
                space_freed=0,
                time_taken=time.time() - start_time,
                errors=errors,
                details={}
            )
            
    async def _optimize_network(self) -> OptimizationResult:
        """Optimize network-related performance"""
        
        start_time = time.time()
        files_processed = 0
        space_freed = 0
        errors = []
        
        try:
            # Clean up network cache files
            network_cache_patterns = [
                '*.tmp',
                '*.download',
                '*_cache.json',
                'network_cache_*'
            ]
            
            for pattern in network_cache_patterns:
                for cache_file in self.project_root.rglob(pattern):
                    try:
                        file_size = cache_file.stat().st_size
                        cache_file.unlink()
                        space_freed += file_size
                        files_processed += 1
                    except Exception as e:
                        errors.append(f"Error cleaning network cache {cache_file}: {e}")
                        
            # Optimize configuration files for network performance
            config_files = [
                self.project_root / 'docker-compose.yml',
                self.project_root / 'backend' / 'requirements.txt',
                self.project_root / 'web_app' / 'package.json',
                self.project_root / 'mobile_app' / 'package.json'
            ]
            
            for config_file in config_files:
                if config_file.exists():
                    files_processed += 1
                    
        except Exception as e:
            errors.append(f"Network optimization error: {e}")
            
        time_taken = time.time() - start_time
        
        return OptimizationResult(
            optimization_type=OptimizationType.NETWORK_OPTIMIZATION,
            files_processed=files_processed,
            space_freed=space_freed,
            time_taken=time_taken,
            errors=errors,
            details={'config_files_processed': len([f for f in config_files if f.exists()])}
        )
        
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        
        if not self.optimization_history:
            return {'message': 'No optimizations performed yet'}
            
        latest_optimization = self.optimization_history[-1]
        
        # Calculate trends
        total_optimizations = len(self.optimization_history)
        total_space_freed = sum(opt['total_space_freed'] for opt in self.optimization_history)
        average_time = sum(opt['total_time'] for opt in self.optimization_history) / total_optimizations
        
        return {
            'latest_optimization': latest_optimization,
            'optimization_history': {
                'total_runs': total_optimizations,
                'total_space_freed': total_space_freed,
                'average_time': average_time,
                'last_run': latest_optimization['timestamp']
            },
            'recommendations': self._generate_optimization_recommendations()
        }
        
    def _generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on analysis"""
        
        recommendations = []
        
        if not self.optimization_history:
            return ['Run initial optimization scan']
            
        latest = self.optimization_history[-1]
        
        # Check for high number of unused files
        if latest['results'].get('component_scan', {}).get('unused_files', 0) > 100:
            recommendations.append("Consider reviewing project structure - many unused files detected")
            
        # Check for large cache sizes
        cache_result = latest['results'].get('cache_optimization', {})
        if cache_result.get('space_freed', 0) > 100 * 1024 * 1024:  # 100MB
            recommendations.append("Implement more aggressive cache cleanup policies")
            
        # Check for database optimization opportunities
        db_result = latest['results'].get('database_optimization', {})
        if db_result.get('space_freed', 0) > 10 * 1024 * 1024:  # 10MB
            recommendations.append("Consider database maintenance schedule")
            
        # Check for memory issues
        memory_result = latest['results'].get('memory_optimization', {})
        if memory_result.get('details', {}).get('objects_collected', 0) > 1000:
            recommendations.append("Review memory management in application code")
            
        if not recommendations:
            recommendations.append("System is well optimized - continue regular maintenance")
            
        return recommendations

# Automated optimization scheduler
class OptimizationScheduler:
    """Schedule and run automated optimizations"""
    
    def __init__(self, optimizer: PerformanceOptimizer):
        self.optimizer = optimizer
        self.schedule_config = {
            'daily_cleanup': True,
            'weekly_deep_clean': True,
            'monthly_analysis': True
        }
        
    async def run_scheduled_optimization(self, optimization_type: str = 'daily'):
        """Run scheduled optimization based on type"""
        
        logger.info(f"Running scheduled optimization: {optimization_type}")
        
        if optimization_type == 'daily':
            # Light cleanup
            result = await self.optimizer._optimize_caches()
            
        elif optimization_type == 'weekly':
            # Medium cleanup
            results = {}
            results['cache'] = await self.optimizer._optimize_caches()
            results['files'] = await self.optimizer._optimize_file_system()
            result = results
            
        elif optimization_type == 'monthly':
            # Full optimization
            result = await self.optimizer.run_comprehensive_optimization()
            
        else:
            raise ValueError(f"Unknown optimization type: {optimization_type}")
            
        logger.info(f"Scheduled optimization {optimization_type} completed")
        return result

if __name__ == "__main__":
    # Example usage
    async def main():
        optimizer = PerformanceOptimizer(".")
        result = await optimizer.run_comprehensive_optimization()
        print(json.dumps(result, indent=2, default=str))
        
    asyncio.run(main())