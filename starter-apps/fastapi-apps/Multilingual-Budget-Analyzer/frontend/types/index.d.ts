// Custom type definitions for missing modules
declare module 'hast' {
  export interface Node {
    type: string;
    [key: string]: any;
  }
}

declare module 'mdast' {
  export interface Node {
    type: string;
    [key: string]: any;
  }
}

declare module 'unist' {
  export interface Node {
    type: string;
    [key: string]: any;
  }
}

declare module 'pbf' {
  export default class Pbf {
    constructor(buf?: ArrayBuffer);
    [key: string]: any;
  }
}

declare module 'supercluster' {
  export default class Supercluster {
    constructor(options?: any);
    [key: string]: any;
  }
}

declare module '@mapbox/point-geometry' {
  export default class Point {
    constructor(x: number, y: number);
    x: number;
    y: number;
    [key: string]: any;
  }
}

declare module '@mapbox/vector-tile' {
  export class VectorTile {
    constructor(pbf: any);
    [key: string]: any;
  }
}

// React types fallback
declare module 'react' {
  export = React;
  export as namespace React;
  namespace React {
    interface Component<P = {}, S = {}> {
      render(): ReactNode;
    }
    interface FunctionComponent<P = {}> {
      (props: P): ReactElement | null;
    }
    type FC<P = {}> = FunctionComponent<P>;
    type ReactNode = any;
    type ReactElement = any;
    interface FormEvent<T = Element> extends Event {
      preventDefault(): void;
    }
    interface KeyboardEvent<T = Element> extends Event {
      key: string;
      shiftKey: boolean;
      preventDefault(): void;
    }
    interface ChangeEvent<T = Element> extends Event {
      target: T;
    }
    interface MouseEvent<T = Element> extends Event {
      preventDefault(): void;
    }
    const useState: <T>(initialState: T) => [T, (newState: T) => void];
    const useEffect: (effect: () => void, deps?: any[]) => void;
    const useRef: <T>(initialValue: T) => { current: T };
  }
}

declare module 'react-dom' {
  export = ReactDOM;
  namespace ReactDOM {
    function render(element: any, container: any): void;
  }
}

// Node.js types fallback
declare module 'node' {
  global {
    namespace NodeJS {
      interface Process {
        env: { [key: string]: string | undefined };
      }
    }
    var process: NodeJS.Process;
  }
} 