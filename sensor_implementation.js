const express = require('express');
const router = express.Router();

// In-memory storage (replace with database in production)
const binData = {};

router.post('/api/update-bin-status', (req, res) => {
    const { binId, fillLevel, odorLevel, status } = req.body;
    
    // Update bin data
    binData[binId] = {
        fillLevel: parseFloat(fillLevel),
        odorLevel,
        status,
        lastUpdated: new Date().toISOString(),
        location: binData[binId]?.location || { lat: 13.0827, lng: 80.2707 } // Preserve location
    };
    
    // Broadcast update to connected clients via WebSocket
    io.emit('binUpdate', {
        binId,
        ...binData[binId]
    });
    
    res.status(200).json({ message: 'Update successful' });
});

module.exports = router;