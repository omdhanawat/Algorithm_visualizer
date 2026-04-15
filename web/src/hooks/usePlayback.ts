import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { normalizeEvent } from '../utils/eventAdapter';
import type { NormalizedEvent } from '../utils/eventAdapter';

export type { NormalizedEvent as AlgoEvent };

export function usePlayback(rawEvents: any[]) {
  // Normalize events, memoized to prevent infinite reset loops
  const events: NormalizedEvent[] = useMemo(() => {
    return rawEvents.map(normalizeEvent);
  }, [rawEvents]);
  
  const [index, setIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000); // ms per step
  const timerRef = useRef<any>(null);

  const next = useCallback(() => {
    if (index < events.length - 1) {
      setIndex((prev) => prev + 1);
    } else {
      setIsPlaying(false);
    }
  }, [index, events.length]);

  const prev = useCallback(() => {
    if (index > 0) {
      setIndex((prev) => prev - 1);
    }
  }, [index]);

  const jumpTo = useCallback((idx: number) => {
    if (idx >= 0 && idx < events.length) {
      setIndex(idx);
    }
  }, [events.length]);

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(next, speed);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, speed, next]);

  // --- RENDER-PHASE RESET ---
  // We reset the index DURING the render if the events change, 
  // ensuring the index is 0 the EXACT same frame as the new data.
  const [prevEvents, setPrevEvents] = useState(events);
  if (events !== prevEvents) {
    setIndex(0);
    setIsPlaying(false);
    setPrevEvents(events);
  }

  return {
    events,
    currentEvent: events[Math.min(index, events.length - 1)] || null,
    index,
    total: events.length,
    isPlaying,
    setIsPlaying,
    speed,
    setSpeed,
    next,
    prev,
    jumpTo,
  };
}
